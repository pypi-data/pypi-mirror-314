from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional

import pandas
from pydantic import HttpUrl, ValidationError
from requests_cache import CachedSession
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed
from tqdm import tqdm

from licitpy.downloader.base import BaseDownloader
from licitpy.parsers.tender import TenderParser
from licitpy.settings import settings
from licitpy.types.attachments import Attachment
from licitpy.types.download import MassiveDownloadSource
from licitpy.types.tender.open_contract import OpenContract
from licitpy.types.tender.status import StatusFromCSV
from licitpy.types.tender.tender import (
    EnrichedTender,
    Question,
    QuestionAnswer,
    TenderFromAPI,
    TenderFromCSV,
)


class TenderDownloader(BaseDownloader):

    def __init__(
        self,
        parser: Optional[TenderParser] = None,
    ) -> None:

        super().__init__()

        self.parser: TenderParser = parser or TenderParser()

    def get_tenders_codes_from_api(
        self, year: int, month: int, skip: int = 0, limit: int | None = None
    ) -> List[TenderFromAPI]:

        # Check if limit is set to 0 or a negative number; if so, return an empty list
        if limit is not None and limit <= 0:
            return []

        # Define the base URL for the API endpoint to fetch tender data
        base_url = "https://api.mercadopublico.cl/APISOCDS/OCDS/listaOCDSAgnoMes"

        # Format the URL for the first request, retrieving up to 1000 records
        url = f"{base_url}/{year}/{month:02}/{skip}/1000"

        # Perform the initial API request and parse the JSON response
        records = self.session.get(url).json()

        # Retrieve the total available records for the given month and year
        total = records["pagination"]["total"]

        # If limit is None, set it to total to fetch all available records
        if limit is None:
            limit = total

        # Extract tender codes from the first batch of data
        tenders = [
            TenderFromAPI(CodigoExterno=str(tender["urlTender"]).split("/")[-1])
            for tender in records["data"]
        ]

        # If the limit is within the first 1000 records, return the filtered tender list
        if limit <= 1000:
            return tenders[:limit]

        # Loop through additional records in blocks of 1000 to fetch the required amount
        for skip in range(1000, total, 1000):

            # If enough records are retrieved, exit the loop
            if len(tenders) >= limit:
                break

            # Format the URL for subsequent requests, always fetching 1000 records per request
            url = f"{base_url}/{year}/{month:02}/{skip}/1000"

            # Perform the API request and parse the JSON response
            records = self.session.get(url).json()

            # Append tender codes from the current batch to the tenders list
            tenders.extend(
                TenderFromAPI(CodigoExterno=str(tender["urlTender"]).split("/")[-1])
                for tender in records["data"]
            )

        # Return the exact number of requested records, sliced to the limit
        return tenders[:limit]

    def get_tenders_from_csv(
        self, year: int, month: int, limit: int | None = None
    ) -> List[TenderFromCSV]:

        columns: List[str] = [
            "CodigoExterno",
            "FechaPublicacion",
            "RegionUnidad",
            "Estado",
            "Nombre",
            "Descripcion",
        ]

        dates_columns = ["FechaPublicacion"]

        df: pandas.DataFrame = self.get_massive_csv_from_zip(
            year, month, columns, dates_columns, MassiveDownloadSource.TENDERS
        )

        # Validate that each 'CodigoExterno' has a unique 'FechaPublicacion'
        if any(df.groupby("CodigoExterno")["FechaPublicacion"].nunique() > 1):
            raise ValueError("Inconsistent publication dates found")

        # The FechaPublicacion comes in a date string format
        df["FechaPublicacion"] = df["FechaPublicacion"].dt.date

        # Strip leading and trailing whitespace from the 'RegionUnidad' column
        df["RegionUnidad"] = df["RegionUnidad"].str.strip()

        # Drop duplicate records based on the 'code' column, keeping the first occurrence
        df = df.drop_duplicates(subset="CodigoExterno", keep="first")

        # Sort the DataFrame by 'opening_date' in ascending order
        # The date is in the following format YYYY-MM-DD (ISO 8601)
        df = df.sort_values(by="FechaPublicacion", ascending=True)

        # Reset the index of the DataFrame after sorting
        df.reset_index(drop=True, inplace=True)

        # If limit is None, set it to the total number of records in the DataFrame
        if limit is None:
            limit = df.shape[0]

        tenders = [
            TenderFromCSV(
                RegionUnidad=tender["RegionUnidad"],
                FechaPublicacion=tender["FechaPublicacion"],
                CodigoExterno=tender["CodigoExterno"],
                Estado=tender["Estado"],
                Nombre=tender["Nombre"],
                Descripcion=tender["Descripcion"],
            )
            for tender in df.to_dict(orient="records")
        ]

        return tenders[:limit]

    @staticmethod
    def is_invalid_contract(contract: Optional[OpenContract]) -> bool:
        return not contract or not contract.records

    @retry(
        retry=retry_if_result(is_invalid_contract),
        wait=wait_fixed(5),
        stop=stop_after_attempt(3),
    )
    def get_tender_ocds_data_from_api(self, code: str) -> OpenContract:

        url = f"https://apis.mercadopublico.cl/OCDS/data/record/{code}"

        response = self.session.get(url)
        data = response.json()

        if "records" not in data and isinstance(self.session, CachedSession):

            with self.session.cache_disabled():

                response = self.session.get(url)
                data = response.json()

                if "records" in data:
                    self.session.cache.save_response(response)

        try:
            return OpenContract(**data)
        except ValidationError as e:
            raise Exception(f"Error parsing OCDS data for tender {code}") from e

    def enrich_tender_with_ocds(self, code: str) -> EnrichedTender:

        data = self.get_tender_ocds_data_from_api(code)

        # 2024-11-16 10:27:00-03:00 <class 'datetime.datetime'>
        opening_date = self.parser.get_tender_opening_date_from_tender_ocds_data(data)

        region = self.parser.get_tender_region_from_tender_ocds_data(data)
        status = self.parser.get_tender_status_from_tender_ocds_data(data)
        title = self.parser.get_tender_title_from_tender_ocds_data(data)
        desc = self.parser.get_tender_description_from_tender_ocds_data(data)

        return EnrichedTender(
            title=title,
            description=desc,
            region=region,
            status=status.name,
            opening_date=opening_date.date(),
        )

    def get_tenders(self, year: int, month: int) -> List[TenderFromCSV]:

        # From the API:
        # [
        #     TenderFromAPI(CodigoExterno='2943-12-LQ24')
        # ]
        tenders_from_api: List[TenderFromAPI] = self.get_tenders_codes_from_api(
            year, month
        )

        # From the CSV.
        # [TenderFromCSV(
        #     CodigoExterno='3149-41-LP24',
        #     RegionUnidad=<Region.II: 'Región de Antofagasta'>,
        #     FechaPublicacion=datetime.date(2024, 11, 1),
        #     Estado=<StatusFromCSV.AWARDED: 'Adjudicada'>,
        #     Nombre='SERVICIO ....',
        #     Descripcion='El objetivo de esta contratación es para amenizar el ...')
        # ]

        tenders_from_csv: List[TenderFromCSV] = self.get_tenders_from_csv(year, month)

        # Filtering tenders that are internal QA tests from Mercado Publico.
        # eg: 500977-191-LS24 : Nombre Unidad : MpOperacionesC

        csv_tender_codes = {
            tender.CodigoExterno
            for tender in tenders_from_csv
            if not tender.CodigoExterno.startswith("500977-")
        }

        api_tenders_missing_date_codes = [
            tender
            for tender in tenders_from_api
            if tender.CodigoExterno not in csv_tender_codes
            and not tender.CodigoExterno.startswith("500977-")
        ]

        api_tenders_enriched: List[TenderFromCSV] = []

        with ThreadPoolExecutor(max_workers=16) as executor:

            futures = {
                executor.submit(
                    self.enrich_tender_with_ocds, tender.CodigoExterno
                ): tender
                for tender in api_tenders_missing_date_codes
            }

            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc=f"Fetching publication dates {year}-{month:02}",
                disable=settings.disable_progress_bar,
            ):

                tender_code: str = futures[future].CodigoExterno
                enrichment = future.result()

                tender = TenderFromCSV(
                    CodigoExterno=tender_code,
                    FechaPublicacion=enrichment.opening_date,
                    RegionUnidad=enrichment.region.value,
                    Estado=StatusFromCSV[enrichment.status.name],
                    Nombre=enrichment.title,
                    Descripcion=enrichment.description,
                )

                api_tenders_enriched.append(tender)

        tenders = tenders_from_csv + api_tenders_enriched

        return sorted(tenders, key=lambda tender: tender.FechaPublicacion, reverse=True)

    def get_tender_url_from_code(self, code: str) -> HttpUrl:
        """
        Generates the tender URL from a given tender code.

        Args:
            code (str): The tender code.

        Returns:
            HttpUrl: The URL pointing to the tender's details page.
        """

        base_url = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx"

        query = (
            self.session.head(f"{base_url}?idlicitacion={code}")
            .headers["Location"]
            .split("qs=")[1]
            .strip()
        )

        return HttpUrl(f"{base_url}?qs={query}")

    def download_attachment(self, url: HttpUrl, attachment: Attachment) -> str:
        return self.download_attachment_from_url(url, attachment)

    def get_tender_questions(self, code: str) -> List[Question]:
        questions = self.session.get(
            "https://www.mercadopublico.cl/Foros/Modules/FNormal/servicesPub.aspx",
            data={"opt": "101", "RFBCode": code},
        ).json()

        
        # eg: Tender : 750301-54-L124
        # [
        #     {
        #         "idP": 1,
        #         "Numero": 6105959,
        #         "Descripcion": "Buenos días\n¿Se puede participar por línea?",
        #         "FechaHora": "05-11-2024 13:08:52",
        #         "Estado": 8,
        #         "RespuestaPublicada": {
        #             "idR": 5581150,
        #             "Descripcion": "SE PUEDE OFERTAR POR LÍNEA SEGÚN LO ESTABLECIDO EN LAS PRESENTES BASES.",
        #             "EstadoR": 4,
        #             "FechaHora": "07-11-2024 12:00:01"
        #         }
        #     }
        # ]

        return [
            Question(
                id=question["Numero"],
                text=str(question["Descripcion"])
                .replace("\n", " ")
                .lower()
                .capitalize(),
                created_at=question["FechaHora"],
                answer=QuestionAnswer(
                    id=question["RespuestaPublicada"]["idR"],
                    text=str(question["RespuestaPublicada"]["Descripcion"])
                    .replace("\n", " ")
                    .lower()
                    .capitalize(),
                    created_at=question["RespuestaPublicada"]["FechaHora"],
                ),
            )
            for question in questions
        ]

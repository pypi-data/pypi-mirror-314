from typing import List

import numpy as np
import pandas

from licitpy.downloader.base import BaseDownloader
from licitpy.types.download import MassiveDownloadSource
from licitpy.types.purchase_order import PurchaseOrderFromCSV


class PurchaseOrderDownloader(BaseDownloader):

    def get_purchase_orders_from_csv(
        self, year: int, month: int, limit: int | None = None
    ) -> List[PurchaseOrderFromCSV]:

        # Note about the commune:
        # In the CSV file, the commune is linked to the column "CiudadUnidadCompra" (AO).
        # Example in CSV format:
        # CiudadUnidadCompra
        # Pudahuel
        # Chol Chol
        # Chol Chol

        columns: List[str] = [
            "Codigo",
            "FechaEnvio",
            "RegionUnidadCompra",
            "CiudadUnidadCompra",
            "Estado",
            "Tipo",
            "Nombre",
            "CodigoLicitacion",
        ]

        dates_columns = ["FechaEnvio"]

        df: pandas.DataFrame = self.get_massive_csv_from_zip(
            year, month, columns, dates_columns, MassiveDownloadSource.PURCHASE_ORDERS
        )

        # Validate that each 'Codigo' has a consistent and unique 'FechaEnvio'
        if any(df.groupby("Codigo")["FechaEnvio"].nunique() > 1):
            raise ValueError("'FechaEnvio' must be unique per 'Codigo'.")

        # Drop duplicate records based on the 'code' column, keeping the first occurrence
        df = df.drop_duplicates(subset="Codigo", keep="first")

        # Sort the DataFrame by 'FechaEnvio' in ascending order
        # The date is in the following format YYYY-MM-DD (ISO 8601)
        df = df.sort_values(by="FechaEnvio", ascending=True)

        # Reset the index of the DataFrame after sorting
        df.reset_index(drop=True, inplace=True)

        # The FechaEnvio comes in a date string format
        df["FechaEnvio"] = df["FechaEnvio"].dt.date

        # Strip leading and trailing whitespace from the 'RegionUnidadCompra' column
        df["RegionUnidadCompra"] = df["RegionUnidadCompra"].str.strip()

        # Remove accents and replace special characters
        # Since we have variations like "Recepcion Conforme" and "Recepción Conforme"
        df["Estado"] = (
            df["Estado"]
            .str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )

        # Fill NaN values in the 'RegionUnidadCompra' column with "Desconocido"
        # There are purchase orders where the Region is not associated.
        # eg: https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=1057402-11253-SE24
        df["RegionUnidadCompra"] = df["RegionUnidadCompra"].fillna("Desconocido")

        # Replace asterisks with NaN values in the 'CiudadUnidadCompra' column
        # eg: https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=4589-830-SE24
        df["CiudadUnidadCompra"] = df["CiudadUnidadCompra"].replace(
            r"^\*\s*$", np.nan, regex=True
        )

        # Replace strings containing only numbers (e.g., "123", " 456 ") in the "CiudadUnidadCompra" column with NaN.
        # Example of a numeric string to be replaced:
        # eg: https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC=1047027-1357-SE24
        df["CiudadUnidadCompra"] = df["CiudadUnidadCompra"].replace(
            r"^\s*\d+\s*$", np.nan, regex=True
        )

        # Fill NaN values in the 'CiudadUnidadCompra' column with "Desconocido"
        df["CiudadUnidadCompra"] = df["CiudadUnidadCompra"].fillna("Desconocido")

        # If limit is None, set it to the total number of records in the DataFrame
        if limit is None:
            limit = df.shape[0]

        purchase_orders = [
            PurchaseOrderFromCSV(
                Codigo=purchase_order["Codigo"],
                FechaEnvio=purchase_order["FechaEnvio"],
                RegionUnidadCompra=purchase_order["RegionUnidadCompra"],
                Estado=purchase_order["Estado"],
                Nombre=purchase_order["Nombre"],
                Tipo=purchase_order["Tipo"],
                CiudadUnidadCompra=purchase_order["CiudadUnidadCompra"],
            )
            for purchase_order in df.to_dict(orient="records")
        ]

        return purchase_orders[:limit]

    def get_purchase_orders(self, year: int, month: int) -> List[PurchaseOrderFromCSV]:
        purchase_orders = self.get_purchase_orders_from_csv(year, month)
        return sorted(purchase_orders, key=lambda po: po.FechaEnvio, reverse=True)

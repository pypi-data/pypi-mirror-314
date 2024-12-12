from enum import Enum
from typing import List

from pydantic import BaseModel, field_validator

from licitpy.types.geography import Region
from licitpy.types.tender.status import StatusFromOpenContract


class Period(BaseModel):
    startDate: str
    endDate: str


class Tender(BaseModel):
    id: str
    title: str
    description: str
    status: StatusFromOpenContract
    tenderPeriod: Period


class PartyRoleEnum(Enum):
    BUYER = "buyer"
    PROCURING_ENTITY = "procuringEntity"
    SUPPLIER = "supplier"
    TENDERER = "tenderer"


class TenderCountryEnum(Enum):
    CL = "Chile"
    US = "Estados Unidos"
    CO = "Colombia"


class Address(BaseModel):
    streetAddress: str | None = None
    region: Region | None = None
    countryName: TenderCountryEnum | None = None

    @field_validator("region", mode="before")
    def strip_region(cls, value: str) -> str:
        return value.strip()


class Party(BaseModel):
    name: str
    id: str
    roles: List[PartyRoleEnum]
    address: Address | None = None


class CompiledRelease(BaseModel):
    ocid: str
    tender: Tender
    parties: List[Party]


class Record(BaseModel):
    ocid: str
    compiledRelease: CompiledRelease


class OpenContract(BaseModel):
    uri: str
    records: List[Record]

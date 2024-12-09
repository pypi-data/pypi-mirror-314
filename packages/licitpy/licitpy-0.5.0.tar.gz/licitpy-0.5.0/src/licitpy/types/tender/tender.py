from datetime import date
from enum import Enum

from pydantic import BaseModel

from licitpy.types.geography import Region
from licitpy.types.tender.status import Status, StatusFromCSV


class Tier(Enum):
    L1 = "L1"  # Less than 100 UTM
    LE = "LE"  # Between 100 and 1,000 UTM
    LP = "LP"  # Between 1,000 and 2,000 UTM
    LQ = "LQ"  # Between 2,000 and 5,000 UTM
    LR = "LR"  # Greater than 5,000 UTM
    LS = "LS"  # Specialized personal services
    O1 = "O1"  # Public bidding for construction projects
    E2 = "E2"  # Private bidding less than 100 UTM
    CO = "CO"  # Private bidding between 100 and 1,000 UTM
    B2 = "B2"  # Private bidding between 1,000 and 2,000 UTM
    H2 = "H2"  # Private bidding between 2,000 and 5,000 UTM
    I2 = "I2"  # Private bidding greater than 5,000 UTM
    O2 = "O2"  # Private bidding for construction projects
    R1 = "R1"  # Purchase order less than 3 UTM (R1)
    R2 = "R2"  # Purchase order less than 3 UTM (R2)
    R3 = "R3"  # ?


class EnrichedTender(BaseModel):
    title: str
    description: str
    region: Region
    status: Status
    opening_date: date


class TenderFromAPI(BaseModel):
    CodigoExterno: str


class TenderFromCSV(BaseModel):
    CodigoExterno: str
    RegionUnidad: Region
    FechaPublicacion: date
    Estado: StatusFromCSV
    Nombre: str
    Descripcion: str

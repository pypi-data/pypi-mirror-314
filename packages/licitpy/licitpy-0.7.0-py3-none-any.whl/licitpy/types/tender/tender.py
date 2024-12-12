from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, field_validator

from licitpy.types.geography import Region
from licitpy.types.tender.status import Status, StatusFromCSV
from licitpy.utils.date import convert_to_datetime


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


class QuestionAnswer(BaseModel):
    id: int
    text: str
    created_at: datetime

    @field_validator("created_at", mode="before")
    def validate_fecha_hora(cls, value: str) -> datetime:
        # "07-11-2024 12:00:01"
        return convert_to_datetime(value, "%d-%m-%Y %H:%M:%S")


class Question(BaseModel):
    id: int
    text: str
    created_at: datetime
    answer: QuestionAnswer

    @field_validator("created_at", mode="before")
    def validate_fecha_hora(cls, value: str) -> datetime:
        # "05-11-2024 13:08:52"
        return convert_to_datetime(value, "%d-%m-%Y %H:%M:%S")


class Unit(Enum):
    BOTTLE = "Botella"
    JAR = "Frasco"
    UNIT = "Unidad"
    KIT = "Kit"
    TUBE = "Tubo"
    ROLL = "Rollo"
    STRIP = "Tira"
    TABLET = "Comprimido"
    AMPOULE = "Ampolla"
    OINTMENT_TUBE = "Pomo"
    GLOBAL = "Global"
    PAIR = "Par"
    SET = "Juego"
    BOX = "Caja"
    PACK = "Pack"
    SHEET = "Pliego"
    DOSE = "Dosis"
    SACK = "Saco"
    BUCKET = "Tineta"
    GALLON = "Galón"
    CARTRIDGE = "Cartucho"
    BAG = "Bolsa"
    KILOGRAM = "kilogramo"
    BAR = "Barra"
    CENTIMETER = "Centímetro"
    CARTON = "Cartón"
    POT = "Pote"
    JERRYCAN = "Bidón"
    YEAR = "Año"
    UNDEFINED = "Unidad no definida"


class Item(BaseModel):
    index: int
    title: str
    category: int
    description: str
    quantity: int
    unit: Unit

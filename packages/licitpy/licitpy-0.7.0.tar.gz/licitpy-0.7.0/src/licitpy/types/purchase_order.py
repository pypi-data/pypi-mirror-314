from datetime import date
from enum import Enum

from pydantic import BaseModel

from licitpy.types.geography import Commune, Region


class Status(Enum):
    # ref: https://ayuda.mercadopublico.cl/preguntasfrecuentes/article/KA-01689/es-es
    ACCEPTED = "Aceptada"
    GOODS_RECEIVED = "Recepcion Conforme"
    SENT_TO_SUPPLIER = "Enviada a proveedor"
    IN_PROCESS = "En proceso"
    CANCELLATION_REQUESTED = "Cancelacion solicitada"


class Type(Enum):
    SE = "SE"
    AG = "AG"
    CM = "CM"
    CC = "CC"


class PurchaseOrderFromCSV(BaseModel):
    Codigo: str
    FechaEnvio: date
    RegionUnidadCompra: Region
    Estado: Status
    Tipo: Type
    Nombre: str
    CiudadUnidadCompra: Commune

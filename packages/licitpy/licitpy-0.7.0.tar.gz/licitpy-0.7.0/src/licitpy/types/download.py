from enum import Enum


class MassiveDownloadSource(str, Enum):
    PURCHASE_ORDERS = "oc"
    TENDERS = "lic"

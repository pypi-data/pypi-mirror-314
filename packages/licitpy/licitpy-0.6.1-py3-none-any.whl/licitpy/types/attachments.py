from enum import Enum
from typing import Callable, Optional

from pydantic import BaseModel, PrivateAttr


class ContentStatus(Enum):
    """
    Enum representing the content's download status.

    Attributes:
        PENDING_DOWNLOAD: Content is ready to be downloaded. Access `.content` to trigger the download.
        AVAILABLE: Content has been downloaded and is ready to use.
    """

    PENDING_DOWNLOAD = "Pending download"
    AVAILABLE = "Downloaded"


class FileType(Enum):

    PDF = "pdf"
    XLSX = "xlsx"
    DOCX = "docx"
    DOC = "doc"
    ZIP = "zip"
    KMZ = "kmz"
    JPG = "jpg"
    RTF = "rtf"
    RAR = "rar"

class Attachment(BaseModel):
    id: str
    name: str
    type: str
    description: str
    size: int
    upload_date: str
    file_type: FileType
    _download_fn: Callable[[], str] = PrivateAttr()
    _content: Optional[str] = PrivateAttr(default=None)

    @property
    def content(self) -> Optional[str]:
        if self._content is None:
            self._content = self._download_fn()
        return self._content

    @property
    def content_status(self) -> ContentStatus:
        if self._content is None:
            return ContentStatus.PENDING_DOWNLOAD
        return ContentStatus.AVAILABLE

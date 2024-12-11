from typing import List

from pydantic import BaseModel

from .argument import Argument


class Handshake(BaseModel):
    AnalyzerName: str
    DisplayName: str
    ArtifactTypes: List[str]
    TopicName: str
    MaxAnalyzeTimeInMinutes: int
    FileInStorageRequired: bool = False
    AutoEnrichmentEnabled: bool = False
    HtmlTemplate: str | None = None
    Arguments: List[Argument] | None = None
    Image: bytes | None = None
    ImageContentType: str | None = None
    ReportLifetimeInDays: int = 0

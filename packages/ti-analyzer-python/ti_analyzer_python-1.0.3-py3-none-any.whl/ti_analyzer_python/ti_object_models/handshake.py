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
    HtmlTemplate: str = ''
    Arguments: List[Argument] = None
    Image: bytes = None
    ImageContentType: str = ''
    ReportLifetimeInDays: int = 0

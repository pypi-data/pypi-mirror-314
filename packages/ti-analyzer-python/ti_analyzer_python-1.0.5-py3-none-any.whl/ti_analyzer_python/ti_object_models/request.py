import uuid
from datetime import datetime

from pydantic import BaseModel


class Request(BaseModel):
    """
    Request to analyzer to check artifact
    :param str AnalyzerName: The name of the analyzer to which the request was sent
    :param str Artifact: The value of the artifact for which analysis is requested
    :param str ArtifactType: The type of the artifact for which analysis is requested
    :param datetime QueueTime: Request queue time
    :param dict Args: Request arguments
    :param uuid.UUID AnalyzerReportId: The identifier of the analyzer report
    """
    AnalyzerName: str | None = None
    Artifact: str | None = None
    ArtifactType: str | None = None
    QueueTime: datetime | None = None
    Args: dict | None = None
    AnalyzerReportId: uuid.UUID = None

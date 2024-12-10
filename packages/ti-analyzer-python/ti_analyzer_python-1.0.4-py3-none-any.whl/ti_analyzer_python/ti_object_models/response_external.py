import uuid

from .response import Response


class ResponseExternal(Response):
    """
    Artifact analysis external result
    :param str AnalyzerName: Analyzer name
    :param uuid.UUID AnalyzerReportId: Analyzer report identifier
    :param str Artifact: Artifact value
    :param str ArtifactType: Type of analyzed artifact
    """
    AnalyzerName: str | None = None
    AnalyzerReportId: uuid.UUID = None
    Artifact: str | None = None
    ArtifactType: str | None = None

from typing import List

from pydantic import BaseModel, JsonValue

from .file_specific_fields import FileSpecificFields
from .network_artifact_specific_fields import NetworkArtifactSpecificFields
from .related_artifact import RelatedArtifact


class Response(BaseModel):
    """
    Artifact analysis result
    :param dict Report: Raw data of the report
    :param str Error: The text of error while processing request
    :param str FirstTimeSeen: Time of first artifact detection
    :param str LastTimeSeen: Time of last artifact detection
    :param int Score: Score of artifact in range from -100 (safe) to 100 (malicious)
    :param List[str] Tags: List of artifact tags
    :param List[RelatedArtifact] RelatedArtifacts: List of related artifacts
    :param List[str] Cves: List of related vulnerabilities
    :param List[str] Mitre: List of related MITRE tactics and techniques
    :param FileSpecificFields FileSpecificFields: Specific fields for file
    :param NetworkArtifactSpecificFields NetworkArtifactSpecificFields: Specific fields for network artifact
    """
    Report: dict | JsonValue | None = None
    Error: str | None = None
    FirstTimeSeen: str | None = None
    LastTimeSeen: str | None = None
    Score: int | None = None
    Tags: List[str] | None = None
    RelatedArtifacts: List[RelatedArtifact] | None = None
    Cves: List[str] | None = None
    Mitre: List[str] | None = None
    FileSpecificFields: FileSpecificFields | None
    NetworkArtifactSpecificFields: NetworkArtifactSpecificFields | None

from pydantic import BaseModel

from .relationship_type import RelationshipType


class RelatedArtifact(BaseModel):
    """
    Artifact related to the main one
    :param str Artifact: Artifact identifier. Might be SHA256, SHA1, MD5, IPv4, IPv6, domain, URL, Email
    :param RelationshipType RelationshipType: The type of relationship
    """
    Artifact: str
    RelationshipType: RelationshipType

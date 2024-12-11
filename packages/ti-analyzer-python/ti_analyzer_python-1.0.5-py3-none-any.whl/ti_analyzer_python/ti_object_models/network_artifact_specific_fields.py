from datetime import datetime

from pydantic import BaseModel


class NetworkArtifactSpecificFields(BaseModel):
    """
    Specific fields for network artifact
    :param str Whois: Whois report
    :param datetime WhoisTime: Whois report time
    :param str Country: Country
    :param str IpNetwork: Network to which the artifact belongs
    :param str Registrar: Registrar of the artifact
    """
    Whois: str | None = None
    WhoisTime: datetime | None = None
    Country: str | None = None
    IpNetwork: str | None = None
    Registrar: str | None = None

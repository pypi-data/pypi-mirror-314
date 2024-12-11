import enum


class TiArtifactTypes(enum.Enum):
    """
    Artifact types supported by RT Protect TI
    """
    File = 'file'
    Domain = 'domain'
    Ip = 'ip'
    Url = 'url'
    Email = 'email'

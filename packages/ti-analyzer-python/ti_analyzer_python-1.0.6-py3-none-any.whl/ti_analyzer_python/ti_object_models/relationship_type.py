import enum


class RelationshipType(enum.Enum):
    """
    Type of relationship between TI entities
    """
    Delivers = 0
    RelatedTo = 1
    Targets = 2
    Uses = 3
    AssociatedTo = 4
    AttributedTo = 5
    Compromises = 6
    OriginatesFrom = 7
    Investigates = 8
    Mitigates = 9
    Remediates = 10
    LocatedAt = 11
    Leveraged = 12
    Indicates = 13
    Suggests = 14
    CommunicatesWith = 15
    ConsistsOf = 16
    Controls = 17
    Has = 18
    Hosts = 19
    Owns = 20
    AuthoredBy = 21
    BeaconsTo = 22
    Downloads = 23
    Drops = 24
    ExfiltratesTo = 25
    Exploits = 26
    VariantOf = 27
    AnalysisOf = 28
    Characterizes = 29
    DynamicAnalysisOf = 30
    StaticAnalysisOf = 31
    Reports = 32
    Impersonates = 33
    Observed = 34

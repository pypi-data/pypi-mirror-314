from typing import List

from pydantic import BaseModel

from .argument_types_enum import ArgumentTypesEnum


class Argument(BaseModel):
    """
    Describes an argument that can be passed to the analyzer when artifact report requested

    :param str Name: Name
    :param ArgumentTypesEnum Type: Type
    :param bool Required: Argument value required for analyzer
    :param List[str] Values: List of possible values. Only for AnalyzerArgumentTypesEnum.Select type
    """
    Name: str
    Type: ArgumentTypesEnum
    Required: bool
    Values: List[str] | None = None

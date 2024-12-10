
from enum import Enum


class OglTextFontFamily(Enum):
    """
    How we specify fonts for Pyut
    """
    SWISS    = 'Swiss'
    MODERN   = 'Modern'
    ROMAN    = 'Roman'
    SCRIPT   = 'Script'
    TELETYPE = 'Teletype'

    @classmethod
    def deSerialize(cls, value: str) -> 'OglTextFontFamily':
        return OglTextFontFamily(value)

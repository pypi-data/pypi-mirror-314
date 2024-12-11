from enum import Enum


class AffectednessEnum(str, Enum):
    NEW = "NEW"
    AFFECTED = "AFFECTED"
    NOTAFFECTED = "NOTAFFECTED"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class ParserOptionsAdditionalPropertyType(str, Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    NUMBER = "number"
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class SystemConfigurationAuthenticationAdditionalPropertyType0Type(str, Enum):
    CREDENTIALS = "credentials"

    def __str__(self) -> str:
        return str(self.value)

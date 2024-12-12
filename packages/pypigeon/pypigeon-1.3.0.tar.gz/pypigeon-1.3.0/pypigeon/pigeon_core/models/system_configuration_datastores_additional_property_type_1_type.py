from enum import Enum


class SystemConfigurationDatastoresAdditionalPropertyType1Type(str, Enum):
    S3 = "s3"

    def __str__(self) -> str:
        return str(self.value)

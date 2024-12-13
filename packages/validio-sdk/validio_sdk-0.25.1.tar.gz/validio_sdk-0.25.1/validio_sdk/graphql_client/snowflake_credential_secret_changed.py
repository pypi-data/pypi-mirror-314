from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class SnowflakeCredentialSecretChanged(BaseModel):
    snowflake_credential_secret_changed: (
        "SnowflakeCredentialSecretChangedSnowflakeCredentialSecretChanged"
    ) = Field(alias="snowflakeCredentialSecretChanged")


class SnowflakeCredentialSecretChangedSnowflakeCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


SnowflakeCredentialSecretChanged.model_rebuild()

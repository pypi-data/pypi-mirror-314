from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateSnowflakeCredential(BaseModel):
    snowflake_credential_create: (
        "CreateSnowflakeCredentialSnowflakeCredentialCreate"
    ) = Field(alias="snowflakeCredentialCreate")


class CreateSnowflakeCredentialSnowflakeCredentialCreate(CredentialCreation):
    pass


CreateSnowflakeCredential.model_rebuild()

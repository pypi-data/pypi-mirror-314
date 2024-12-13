from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateDbtCoreCredential(BaseModel):
    dbt_core_credential_create: "CreateDbtCoreCredentialDbtCoreCredentialCreate" = (
        Field(alias="dbtCoreCredentialCreate")
    )


class CreateDbtCoreCredentialDbtCoreCredentialCreate(CredentialCreation):
    pass


CreateDbtCoreCredential.model_rebuild()

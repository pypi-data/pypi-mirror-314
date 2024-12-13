from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateDbtCoreCredential(BaseModel):
    dbt_core_credential_update: "UpdateDbtCoreCredentialDbtCoreCredentialUpdate" = (
        Field(alias="dbtCoreCredentialUpdate")
    )


class UpdateDbtCoreCredentialDbtCoreCredentialUpdate(CredentialUpdate):
    pass


UpdateDbtCoreCredential.model_rebuild()

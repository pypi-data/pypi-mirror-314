from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateAzureSynapseSqlCredential(BaseModel):
    azure_synapse_sql_credential_create: (
        "CreateAzureSynapseSqlCredentialAzureSynapseSqlCredentialCreate"
    ) = Field(alias="azureSynapseSqlCredentialCreate")


class CreateAzureSynapseSqlCredentialAzureSynapseSqlCredentialCreate(
    CredentialCreation
):
    pass


CreateAzureSynapseSqlCredential.model_rebuild()

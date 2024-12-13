from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateAzureSynapseSqlCredential(BaseModel):
    azure_synapse_sql_credential_update: (
        "UpdateAzureSynapseSqlCredentialAzureSynapseSqlCredentialUpdate"
    ) = Field(alias="azureSynapseSqlCredentialUpdate")


class UpdateAzureSynapseSqlCredentialAzureSynapseSqlCredentialUpdate(CredentialUpdate):
    pass


UpdateAzureSynapseSqlCredential.model_rebuild()

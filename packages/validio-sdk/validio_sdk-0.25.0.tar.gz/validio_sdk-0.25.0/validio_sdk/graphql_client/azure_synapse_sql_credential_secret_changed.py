from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class AzureSynapseSqlCredentialSecretChanged(BaseModel):
    azure_synapse_sql_credential_secret_changed: (
        "AzureSynapseSqlCredentialSecretChangedAzureSynapseSqlCredentialSecretChanged"
    ) = Field(alias="azureSynapseSqlCredentialSecretChanged")


class AzureSynapseSqlCredentialSecretChangedAzureSynapseSqlCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


AzureSynapseSqlCredentialSecretChanged.model_rebuild()

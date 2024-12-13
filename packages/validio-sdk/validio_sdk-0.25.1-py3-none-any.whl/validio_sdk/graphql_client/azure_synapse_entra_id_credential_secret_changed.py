from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class AzureSynapseEntraIdCredentialSecretChanged(BaseModel):
    azure_synapse_entra_id_credential_secret_changed: (
        "AzureSynapseEntraIdCredentialSecretChangedAzureSynapseEntraIdCredentialSecretChanged"
    ) = Field(alias="azureSynapseEntraIdCredentialSecretChanged")


class AzureSynapseEntraIdCredentialSecretChangedAzureSynapseEntraIdCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


AzureSynapseEntraIdCredentialSecretChanged.model_rebuild()

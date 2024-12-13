from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateAzureSynapseEntraIdCredential(BaseModel):
    azure_synapse_entra_id_credential_update: (
        "UpdateAzureSynapseEntraIdCredentialAzureSynapseEntraIdCredentialUpdate"
    ) = Field(alias="azureSynapseEntraIdCredentialUpdate")


class UpdateAzureSynapseEntraIdCredentialAzureSynapseEntraIdCredentialUpdate(
    CredentialUpdate
):
    pass


UpdateAzureSynapseEntraIdCredential.model_rebuild()

from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateAzureSynapseEntraIdCredential(BaseModel):
    azure_synapse_entra_id_credential_create: (
        "CreateAzureSynapseEntraIdCredentialAzureSynapseEntraIdCredentialCreate"
    ) = Field(alias="azureSynapseEntraIdCredentialCreate")


class CreateAzureSynapseEntraIdCredentialAzureSynapseEntraIdCredentialCreate(
    CredentialCreation
):
    pass


CreateAzureSynapseEntraIdCredential.model_rebuild()

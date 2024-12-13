from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class GcpCredentialSecretChanged(BaseModel):
    gcp_credential_secret_changed: (
        "GcpCredentialSecretChangedGcpCredentialSecretChanged"
    ) = Field(alias="gcpCredentialSecretChanged")


class GcpCredentialSecretChangedGcpCredentialSecretChanged(CredentialSecretChanged):
    pass


GcpCredentialSecretChanged.model_rebuild()

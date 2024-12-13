from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateTableauConnectedAppCredential(BaseModel):
    tableau_connected_app_credential_update: (
        "UpdateTableauConnectedAppCredentialTableauConnectedAppCredentialUpdate"
    ) = Field(alias="tableauConnectedAppCredentialUpdate")


class UpdateTableauConnectedAppCredentialTableauConnectedAppCredentialUpdate(
    CredentialUpdate
):
    pass


UpdateTableauConnectedAppCredential.model_rebuild()

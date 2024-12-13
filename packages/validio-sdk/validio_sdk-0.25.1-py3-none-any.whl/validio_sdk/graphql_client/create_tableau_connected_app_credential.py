from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateTableauConnectedAppCredential(BaseModel):
    tableau_connected_app_credential_create: (
        "CreateTableauConnectedAppCredentialTableauConnectedAppCredentialCreate"
    ) = Field(alias="tableauConnectedAppCredentialCreate")


class CreateTableauConnectedAppCredentialTableauConnectedAppCredentialCreate(
    CredentialCreation
):
    pass


CreateTableauConnectedAppCredential.model_rebuild()

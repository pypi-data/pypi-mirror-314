from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class TableauConnectedAppCredentialSecretChanged(BaseModel):
    tableau_connected_app_credential_secret_changed: (
        "TableauConnectedAppCredentialSecretChangedTableauConnectedAppCredentialSecretChanged"
    ) = Field(alias="tableauConnectedAppCredentialSecretChanged")


class TableauConnectedAppCredentialSecretChangedTableauConnectedAppCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


TableauConnectedAppCredentialSecretChanged.model_rebuild()

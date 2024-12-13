from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class TableauPersonalAccessTokenCredentialSecretChanged(BaseModel):
    tableau_personal_access_token_credential_secret_changed: (
        "TableauPersonalAccessTokenCredentialSecretChangedTableauPersonalAccessTokenCredentialSecretChanged"
    ) = Field(alias="tableauPersonalAccessTokenCredentialSecretChanged")


class TableauPersonalAccessTokenCredentialSecretChangedTableauPersonalAccessTokenCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


TableauPersonalAccessTokenCredentialSecretChanged.model_rebuild()

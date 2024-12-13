from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateTableauPersonalAccessTokenCredential(BaseModel):
    tableau_personal_access_token_credential_update: (
        "UpdateTableauPersonalAccessTokenCredentialTableauPersonalAccessTokenCredentialUpdate"
    ) = Field(alias="tableauPersonalAccessTokenCredentialUpdate")


class UpdateTableauPersonalAccessTokenCredentialTableauPersonalAccessTokenCredentialUpdate(
    CredentialUpdate
):
    pass


UpdateTableauPersonalAccessTokenCredential.model_rebuild()

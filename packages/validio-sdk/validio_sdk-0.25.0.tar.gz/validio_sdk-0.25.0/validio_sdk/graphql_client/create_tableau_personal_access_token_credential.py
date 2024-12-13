from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateTableauPersonalAccessTokenCredential(BaseModel):
    tableau_personal_access_token_credential_create: (
        "CreateTableauPersonalAccessTokenCredentialTableauPersonalAccessTokenCredentialCreate"
    ) = Field(alias="tableauPersonalAccessTokenCredentialCreate")


class CreateTableauPersonalAccessTokenCredentialTableauPersonalAccessTokenCredentialCreate(
    CredentialCreation
):
    pass


CreateTableauPersonalAccessTokenCredential.model_rebuild()

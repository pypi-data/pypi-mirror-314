from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateLookerCredential(BaseModel):
    looker_credential_update: "UpdateLookerCredentialLookerCredentialUpdate" = Field(
        alias="lookerCredentialUpdate"
    )


class UpdateLookerCredentialLookerCredentialUpdate(CredentialUpdate):
    pass


UpdateLookerCredential.model_rebuild()

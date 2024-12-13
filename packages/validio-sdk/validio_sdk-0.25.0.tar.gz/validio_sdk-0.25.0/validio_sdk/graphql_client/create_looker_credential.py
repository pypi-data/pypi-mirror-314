from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateLookerCredential(BaseModel):
    looker_credential_create: "CreateLookerCredentialLookerCredentialCreate" = Field(
        alias="lookerCredentialCreate"
    )


class CreateLookerCredentialLookerCredentialCreate(CredentialCreation):
    pass


CreateLookerCredential.model_rebuild()

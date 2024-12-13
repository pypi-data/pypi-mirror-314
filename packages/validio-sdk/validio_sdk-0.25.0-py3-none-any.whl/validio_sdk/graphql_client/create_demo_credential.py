from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateDemoCredential(BaseModel):
    demo_credential_create: "CreateDemoCredentialDemoCredentialCreate" = Field(
        alias="demoCredentialCreate"
    )


class CreateDemoCredentialDemoCredentialCreate(CredentialCreation):
    pass


CreateDemoCredential.model_rebuild()

from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateDemoCredential(BaseModel):
    demo_credential_update: "UpdateDemoCredentialDemoCredentialUpdate" = Field(
        alias="demoCredentialUpdate"
    )


class UpdateDemoCredentialDemoCredentialUpdate(CredentialUpdate):
    pass


UpdateDemoCredential.model_rebuild()

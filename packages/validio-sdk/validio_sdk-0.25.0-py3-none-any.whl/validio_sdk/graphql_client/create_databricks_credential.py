from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateDatabricksCredential(BaseModel):
    databricks_credential_create: (
        "CreateDatabricksCredentialDatabricksCredentialCreate"
    ) = Field(alias="databricksCredentialCreate")


class CreateDatabricksCredentialDatabricksCredentialCreate(CredentialCreation):
    pass


CreateDatabricksCredential.model_rebuild()

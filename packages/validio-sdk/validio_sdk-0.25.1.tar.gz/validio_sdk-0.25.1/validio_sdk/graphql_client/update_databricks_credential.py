from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateDatabricksCredential(BaseModel):
    databricks_credential_update: (
        "UpdateDatabricksCredentialDatabricksCredentialUpdate"
    ) = Field(alias="databricksCredentialUpdate")


class UpdateDatabricksCredentialDatabricksCredentialUpdate(CredentialUpdate):
    pass


UpdateDatabricksCredential.model_rebuild()

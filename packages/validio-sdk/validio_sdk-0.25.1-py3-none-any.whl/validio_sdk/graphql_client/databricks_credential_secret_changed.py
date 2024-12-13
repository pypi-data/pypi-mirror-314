from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class DatabricksCredentialSecretChanged(BaseModel):
    databricks_credential_secret_changed: (
        "DatabricksCredentialSecretChangedDatabricksCredentialSecretChanged"
    ) = Field(alias="databricksCredentialSecretChanged")


class DatabricksCredentialSecretChangedDatabricksCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


DatabricksCredentialSecretChanged.model_rebuild()

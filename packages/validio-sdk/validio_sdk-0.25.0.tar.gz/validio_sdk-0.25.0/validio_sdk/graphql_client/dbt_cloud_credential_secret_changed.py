from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class DbtCloudCredentialSecretChanged(BaseModel):
    dbt_cloud_credential_secret_changed: (
        "DbtCloudCredentialSecretChangedDbtCloudCredentialSecretChanged"
    ) = Field(alias="dbtCloudCredentialSecretChanged")


class DbtCloudCredentialSecretChangedDbtCloudCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


DbtCloudCredentialSecretChanged.model_rebuild()

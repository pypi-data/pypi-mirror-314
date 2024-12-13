from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateDbtCloudCredential(BaseModel):
    dbt_cloud_credential_update: "UpdateDbtCloudCredentialDbtCloudCredentialUpdate" = (
        Field(alias="dbtCloudCredentialUpdate")
    )


class UpdateDbtCloudCredentialDbtCloudCredentialUpdate(CredentialUpdate):
    pass


UpdateDbtCloudCredential.model_rebuild()

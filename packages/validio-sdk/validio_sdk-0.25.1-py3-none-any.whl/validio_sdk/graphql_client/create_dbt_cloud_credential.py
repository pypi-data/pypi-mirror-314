from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateDbtCloudCredential(BaseModel):
    dbt_cloud_credential_create: "CreateDbtCloudCredentialDbtCloudCredentialCreate" = (
        Field(alias="dbtCloudCredentialCreate")
    )


class CreateDbtCloudCredentialDbtCloudCredentialCreate(CredentialCreation):
    pass


CreateDbtCloudCredential.model_rebuild()

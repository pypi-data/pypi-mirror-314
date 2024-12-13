from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class AwsAthenaCredentialSecretChanged(BaseModel):
    aws_athena_credential_secret_changed: (
        "AwsAthenaCredentialSecretChangedAwsAthenaCredentialSecretChanged"
    ) = Field(alias="awsAthenaCredentialSecretChanged")


class AwsAthenaCredentialSecretChangedAwsAthenaCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


AwsAthenaCredentialSecretChanged.model_rebuild()

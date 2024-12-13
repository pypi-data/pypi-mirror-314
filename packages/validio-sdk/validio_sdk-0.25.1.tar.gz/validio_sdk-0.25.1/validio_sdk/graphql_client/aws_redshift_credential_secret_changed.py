from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class AwsRedshiftCredentialSecretChanged(BaseModel):
    aws_redshift_credential_secret_changed: (
        "AwsRedshiftCredentialSecretChangedAwsRedshiftCredentialSecretChanged"
    ) = Field(alias="awsRedshiftCredentialSecretChanged")


class AwsRedshiftCredentialSecretChangedAwsRedshiftCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


AwsRedshiftCredentialSecretChanged.model_rebuild()

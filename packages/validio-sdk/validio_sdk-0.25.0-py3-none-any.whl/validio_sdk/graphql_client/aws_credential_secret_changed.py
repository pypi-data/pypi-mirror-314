from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class AwsCredentialSecretChanged(BaseModel):
    aws_credential_secret_changed: (
        "AwsCredentialSecretChangedAwsCredentialSecretChanged"
    ) = Field(alias="awsCredentialSecretChanged")


class AwsCredentialSecretChangedAwsCredentialSecretChanged(CredentialSecretChanged):
    pass


AwsCredentialSecretChanged.model_rebuild()

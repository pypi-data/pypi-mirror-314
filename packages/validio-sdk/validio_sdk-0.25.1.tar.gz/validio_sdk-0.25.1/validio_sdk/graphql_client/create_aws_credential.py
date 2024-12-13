from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateAwsCredential(BaseModel):
    aws_credential_create: "CreateAwsCredentialAwsCredentialCreate" = Field(
        alias="awsCredentialCreate"
    )


class CreateAwsCredentialAwsCredentialCreate(CredentialCreation):
    pass


CreateAwsCredential.model_rebuild()

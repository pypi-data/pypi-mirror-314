from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateAwsRedshiftCredential(BaseModel):
    aws_redshift_credential_create: (
        "CreateAwsRedshiftCredentialAwsRedshiftCredentialCreate"
    ) = Field(alias="awsRedshiftCredentialCreate")


class CreateAwsRedshiftCredentialAwsRedshiftCredentialCreate(CredentialCreation):
    pass


CreateAwsRedshiftCredential.model_rebuild()

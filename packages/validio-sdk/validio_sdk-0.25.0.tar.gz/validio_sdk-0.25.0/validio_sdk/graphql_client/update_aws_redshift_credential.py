from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateAwsRedshiftCredential(BaseModel):
    aws_redshift_credential_update: (
        "UpdateAwsRedshiftCredentialAwsRedshiftCredentialUpdate"
    ) = Field(alias="awsRedshiftCredentialUpdate")


class UpdateAwsRedshiftCredentialAwsRedshiftCredentialUpdate(CredentialUpdate):
    pass


UpdateAwsRedshiftCredential.model_rebuild()

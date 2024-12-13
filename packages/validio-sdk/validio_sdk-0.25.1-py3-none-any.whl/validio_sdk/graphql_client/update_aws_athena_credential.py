from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateAwsAthenaCredential(BaseModel):
    aws_athena_credential_update: (
        "UpdateAwsAthenaCredentialAwsAthenaCredentialUpdate"
    ) = Field(alias="awsAthenaCredentialUpdate")


class UpdateAwsAthenaCredentialAwsAthenaCredentialUpdate(CredentialUpdate):
    pass


UpdateAwsAthenaCredential.model_rebuild()

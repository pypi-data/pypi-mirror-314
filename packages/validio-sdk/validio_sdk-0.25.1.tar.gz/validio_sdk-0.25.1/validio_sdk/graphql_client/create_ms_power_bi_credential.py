from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateMsPowerBiCredential(BaseModel):
    ms_power_bi_credential_create: (
        "CreateMsPowerBiCredentialMsPowerBiCredentialCreate"
    ) = Field(alias="msPowerBiCredentialCreate")


class CreateMsPowerBiCredentialMsPowerBiCredentialCreate(CredentialCreation):
    pass


CreateMsPowerBiCredential.model_rebuild()

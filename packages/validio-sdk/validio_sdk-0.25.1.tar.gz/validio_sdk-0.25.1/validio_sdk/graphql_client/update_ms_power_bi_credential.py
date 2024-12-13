from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateMsPowerBiCredential(BaseModel):
    ms_power_bi_credential_update: (
        "UpdateMsPowerBiCredentialMsPowerBiCredentialUpdate"
    ) = Field(alias="msPowerBiCredentialUpdate")


class UpdateMsPowerBiCredentialMsPowerBiCredentialUpdate(CredentialUpdate):
    pass


UpdateMsPowerBiCredential.model_rebuild()

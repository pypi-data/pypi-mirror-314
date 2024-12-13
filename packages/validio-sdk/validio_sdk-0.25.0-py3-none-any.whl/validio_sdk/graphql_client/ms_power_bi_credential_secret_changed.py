from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class MsPowerBiCredentialSecretChanged(BaseModel):
    ms_power_bi_credential_secret_changed: (
        "MsPowerBiCredentialSecretChangedMsPowerBiCredentialSecretChanged"
    ) = Field(alias="msPowerBiCredentialSecretChanged")


class MsPowerBiCredentialSecretChangedMsPowerBiCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


MsPowerBiCredentialSecretChanged.model_rebuild()

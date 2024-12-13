from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class LookerCredentialSecretChanged(BaseModel):
    looker_credential_secret_changed: (
        "LookerCredentialSecretChangedLookerCredentialSecretChanged"
    ) = Field(alias="lookerCredentialSecretChanged")


class LookerCredentialSecretChangedLookerCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


LookerCredentialSecretChanged.model_rebuild()

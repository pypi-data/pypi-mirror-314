from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class ClickHouseCredentialSecretChanged(BaseModel):
    click_house_credential_secret_changed: (
        "ClickHouseCredentialSecretChangedClickHouseCredentialSecretChanged"
    ) = Field(alias="clickHouseCredentialSecretChanged")


class ClickHouseCredentialSecretChangedClickHouseCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


ClickHouseCredentialSecretChanged.model_rebuild()

from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class KafkaSslCredentialSecretChanged(BaseModel):
    kafka_ssl_credential_secret_changed: (
        "KafkaSslCredentialSecretChangedKafkaSslCredentialSecretChanged"
    ) = Field(alias="kafkaSslCredentialSecretChanged")


class KafkaSslCredentialSecretChangedKafkaSslCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


KafkaSslCredentialSecretChanged.model_rebuild()

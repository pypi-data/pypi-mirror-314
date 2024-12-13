from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class KafkaSaslSslPlainCredentialSecretChanged(BaseModel):
    kafka_sasl_ssl_plain_credential_secret_changed: (
        "KafkaSaslSslPlainCredentialSecretChangedKafkaSaslSslPlainCredentialSecretChanged"
    ) = Field(alias="kafkaSaslSslPlainCredentialSecretChanged")


class KafkaSaslSslPlainCredentialSecretChangedKafkaSaslSslPlainCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


KafkaSaslSslPlainCredentialSecretChanged.model_rebuild()

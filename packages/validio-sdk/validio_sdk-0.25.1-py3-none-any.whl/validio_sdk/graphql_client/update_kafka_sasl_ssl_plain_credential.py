from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateKafkaSaslSslPlainCredential(BaseModel):
    kafka_sasl_ssl_plain_credential_update: (
        "UpdateKafkaSaslSslPlainCredentialKafkaSaslSslPlainCredentialUpdate"
    ) = Field(alias="kafkaSaslSslPlainCredentialUpdate")


class UpdateKafkaSaslSslPlainCredentialKafkaSaslSslPlainCredentialUpdate(
    CredentialUpdate
):
    pass


UpdateKafkaSaslSslPlainCredential.model_rebuild()

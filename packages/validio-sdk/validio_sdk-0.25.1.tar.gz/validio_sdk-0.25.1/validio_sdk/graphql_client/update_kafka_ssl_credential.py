from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateKafkaSslCredential(BaseModel):
    kafka_ssl_credential_update: "UpdateKafkaSslCredentialKafkaSslCredentialUpdate" = (
        Field(alias="kafkaSslCredentialUpdate")
    )


class UpdateKafkaSslCredentialKafkaSslCredentialUpdate(CredentialUpdate):
    pass


UpdateKafkaSslCredential.model_rebuild()

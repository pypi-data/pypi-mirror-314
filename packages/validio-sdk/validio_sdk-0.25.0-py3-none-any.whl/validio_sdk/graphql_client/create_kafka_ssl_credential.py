from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateKafkaSslCredential(BaseModel):
    kafka_ssl_credential_create: "CreateKafkaSslCredentialKafkaSslCredentialCreate" = (
        Field(alias="kafkaSslCredentialCreate")
    )


class CreateKafkaSslCredentialKafkaSslCredentialCreate(CredentialCreation):
    pass


CreateKafkaSslCredential.model_rebuild()

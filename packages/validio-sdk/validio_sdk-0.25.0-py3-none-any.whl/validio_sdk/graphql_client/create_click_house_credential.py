from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateClickHouseCredential(BaseModel):
    click_house_credential_create: (
        "CreateClickHouseCredentialClickHouseCredentialCreate"
    ) = Field(alias="clickHouseCredentialCreate")


class CreateClickHouseCredentialClickHouseCredentialCreate(CredentialCreation):
    pass


CreateClickHouseCredential.model_rebuild()

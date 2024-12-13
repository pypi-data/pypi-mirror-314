from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateClickHouseCredential(BaseModel):
    click_house_credential_update: (
        "UpdateClickHouseCredentialClickHouseCredentialUpdate"
    ) = Field(alias="clickHouseCredentialUpdate")


class UpdateClickHouseCredentialClickHouseCredentialUpdate(CredentialUpdate):
    pass


UpdateClickHouseCredential.model_rebuild()

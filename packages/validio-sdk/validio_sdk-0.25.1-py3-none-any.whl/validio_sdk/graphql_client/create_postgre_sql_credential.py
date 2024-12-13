from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreatePostgreSqlCredential(BaseModel):
    postgre_sql_credential_create: (
        "CreatePostgreSqlCredentialPostgreSqlCredentialCreate"
    ) = Field(alias="postgreSqlCredentialCreate")


class CreatePostgreSqlCredentialPostgreSqlCredentialCreate(CredentialCreation):
    pass


CreatePostgreSqlCredential.model_rebuild()

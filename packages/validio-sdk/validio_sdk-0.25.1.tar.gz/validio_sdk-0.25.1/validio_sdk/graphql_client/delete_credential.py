from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteCredential(BaseModel):
    credentials_delete: "DeleteCredentialCredentialsDelete" = Field(
        alias="credentialsDelete"
    )


class DeleteCredentialCredentialsDelete(BaseModel):
    errors: List["DeleteCredentialCredentialsDeleteErrors"]


class DeleteCredentialCredentialsDeleteErrors(ErrorDetails):
    pass


DeleteCredential.model_rebuild()
DeleteCredentialCredentialsDelete.model_rebuild()

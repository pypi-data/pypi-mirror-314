from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteCredentials(BaseModel):
    credentials_delete: "DeleteCredentialsCredentialsDelete" = Field(
        alias="credentialsDelete"
    )


class DeleteCredentialsCredentialsDelete(BaseModel):
    errors: List["DeleteCredentialsCredentialsDeleteErrors"]


class DeleteCredentialsCredentialsDeleteErrors(ErrorDetails):
    pass


DeleteCredentials.model_rebuild()
DeleteCredentialsCredentialsDelete.model_rebuild()

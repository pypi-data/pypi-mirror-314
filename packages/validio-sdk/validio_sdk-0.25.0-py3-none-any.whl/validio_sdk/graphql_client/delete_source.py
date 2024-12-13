from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteSource(BaseModel):
    sources_delete: "DeleteSourceSourcesDelete" = Field(alias="sourcesDelete")


class DeleteSourceSourcesDelete(BaseModel):
    errors: List["DeleteSourceSourcesDeleteErrors"]


class DeleteSourceSourcesDeleteErrors(ErrorDetails):
    pass


DeleteSource.model_rebuild()
DeleteSourceSourcesDelete.model_rebuild()

from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteFilter(BaseModel):
    filters_delete: "DeleteFilterFiltersDelete" = Field(alias="filtersDelete")


class DeleteFilterFiltersDelete(BaseModel):
    errors: List["DeleteFilterFiltersDeleteErrors"]


class DeleteFilterFiltersDeleteErrors(ErrorDetails):
    pass


DeleteFilter.model_rebuild()
DeleteFilterFiltersDelete.model_rebuild()

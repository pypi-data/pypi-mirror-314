from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteFilters(BaseModel):
    filters_delete: "DeleteFiltersFiltersDelete" = Field(alias="filtersDelete")


class DeleteFiltersFiltersDelete(BaseModel):
    errors: List["DeleteFiltersFiltersDeleteErrors"]


class DeleteFiltersFiltersDeleteErrors(ErrorDetails):
    pass


DeleteFilters.model_rebuild()
DeleteFiltersFiltersDelete.model_rebuild()

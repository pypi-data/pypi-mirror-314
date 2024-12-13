from pydantic import Field

from .base_model import BaseModel
from .fragments import FilterUpdate


class UpdateStringFilter(BaseModel):
    string_filter_update: "UpdateStringFilterStringFilterUpdate" = Field(
        alias="stringFilterUpdate"
    )


class UpdateStringFilterStringFilterUpdate(FilterUpdate):
    pass


UpdateStringFilter.model_rebuild()

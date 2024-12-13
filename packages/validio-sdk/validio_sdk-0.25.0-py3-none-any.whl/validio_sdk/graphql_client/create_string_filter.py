from pydantic import Field

from .base_model import BaseModel
from .fragments import FilterCreation


class CreateStringFilter(BaseModel):
    string_filter_create: "CreateStringFilterStringFilterCreate" = Field(
        alias="stringFilterCreate"
    )


class CreateStringFilterStringFilterCreate(FilterCreation):
    pass


CreateStringFilter.model_rebuild()

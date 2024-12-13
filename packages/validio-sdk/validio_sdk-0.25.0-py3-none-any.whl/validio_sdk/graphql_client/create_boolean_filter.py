from pydantic import Field

from .base_model import BaseModel
from .fragments import FilterCreation


class CreateBooleanFilter(BaseModel):
    boolean_filter_create: "CreateBooleanFilterBooleanFilterCreate" = Field(
        alias="booleanFilterCreate"
    )


class CreateBooleanFilterBooleanFilterCreate(FilterCreation):
    pass


CreateBooleanFilter.model_rebuild()

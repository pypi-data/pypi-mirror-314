from pydantic import Field

from .base_model import BaseModel
from .fragments import FilterCreation


class CreateNullFilter(BaseModel):
    null_filter_create: "CreateNullFilterNullFilterCreate" = Field(
        alias="nullFilterCreate"
    )


class CreateNullFilterNullFilterCreate(FilterCreation):
    pass


CreateNullFilter.model_rebuild()

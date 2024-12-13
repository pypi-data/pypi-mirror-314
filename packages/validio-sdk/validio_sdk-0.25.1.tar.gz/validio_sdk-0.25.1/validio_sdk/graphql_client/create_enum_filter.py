from pydantic import Field

from .base_model import BaseModel
from .fragments import FilterCreation


class CreateEnumFilter(BaseModel):
    enum_filter_create: "CreateEnumFilterEnumFilterCreate" = Field(
        alias="enumFilterCreate"
    )


class CreateEnumFilterEnumFilterCreate(FilterCreation):
    pass


CreateEnumFilter.model_rebuild()

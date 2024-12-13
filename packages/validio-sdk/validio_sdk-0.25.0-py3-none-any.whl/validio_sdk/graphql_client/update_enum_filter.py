from pydantic import Field

from .base_model import BaseModel
from .fragments import FilterUpdate


class UpdateEnumFilter(BaseModel):
    enum_filter_update: "UpdateEnumFilterEnumFilterUpdate" = Field(
        alias="enumFilterUpdate"
    )


class UpdateEnumFilterEnumFilterUpdate(FilterUpdate):
    pass


UpdateEnumFilter.model_rebuild()

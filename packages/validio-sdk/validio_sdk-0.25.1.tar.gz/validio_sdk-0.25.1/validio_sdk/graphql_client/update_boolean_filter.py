from pydantic import Field

from .base_model import BaseModel
from .fragments import FilterUpdate


class UpdateBooleanFilter(BaseModel):
    boolean_filter_update: "UpdateBooleanFilterBooleanFilterUpdate" = Field(
        alias="booleanFilterUpdate"
    )


class UpdateBooleanFilterBooleanFilterUpdate(FilterUpdate):
    pass


UpdateBooleanFilter.model_rebuild()

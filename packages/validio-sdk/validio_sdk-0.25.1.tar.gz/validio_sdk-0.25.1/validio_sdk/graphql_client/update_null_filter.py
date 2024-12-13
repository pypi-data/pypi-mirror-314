from pydantic import Field

from .base_model import BaseModel
from .fragments import FilterUpdate


class UpdateNullFilter(BaseModel):
    null_filter_update: "UpdateNullFilterNullFilterUpdate" = Field(
        alias="nullFilterUpdate"
    )


class UpdateNullFilterNullFilterUpdate(FilterUpdate):
    pass


UpdateNullFilter.model_rebuild()

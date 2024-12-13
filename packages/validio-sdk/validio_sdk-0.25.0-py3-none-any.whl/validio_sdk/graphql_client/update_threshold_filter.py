from pydantic import Field

from .base_model import BaseModel
from .fragments import FilterUpdate


class UpdateThresholdFilter(BaseModel):
    threshold_filter_update: "UpdateThresholdFilterThresholdFilterUpdate" = Field(
        alias="thresholdFilterUpdate"
    )


class UpdateThresholdFilterThresholdFilterUpdate(FilterUpdate):
    pass


UpdateThresholdFilter.model_rebuild()

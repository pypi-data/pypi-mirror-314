from pydantic import Field

from .base_model import BaseModel
from .fragments import FilterCreation


class CreateThresholdFilter(BaseModel):
    threshold_filter_create: "CreateThresholdFilterThresholdFilterCreate" = Field(
        alias="thresholdFilterCreate"
    )


class CreateThresholdFilterThresholdFilterCreate(FilterCreation):
    pass


CreateThresholdFilter.model_rebuild()

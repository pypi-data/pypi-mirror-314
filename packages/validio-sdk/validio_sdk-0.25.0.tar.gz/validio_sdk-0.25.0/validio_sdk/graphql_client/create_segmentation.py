from pydantic import Field

from .base_model import BaseModel
from .fragments import SegmentationCreation


class CreateSegmentation(BaseModel):
    segmentation_create: "CreateSegmentationSegmentationCreate" = Field(
        alias="segmentationCreate"
    )


class CreateSegmentationSegmentationCreate(SegmentationCreation):
    pass


CreateSegmentation.model_rebuild()

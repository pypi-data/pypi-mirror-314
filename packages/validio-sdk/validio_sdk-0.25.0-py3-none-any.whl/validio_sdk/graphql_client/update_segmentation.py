from pydantic import Field

from .base_model import BaseModel
from .fragments import SegmentationUpdate


class UpdateSegmentation(BaseModel):
    segmentation_update: "UpdateSegmentationSegmentationUpdate" = Field(
        alias="segmentationUpdate"
    )


class UpdateSegmentationSegmentationUpdate(SegmentationUpdate):
    pass


UpdateSegmentation.model_rebuild()

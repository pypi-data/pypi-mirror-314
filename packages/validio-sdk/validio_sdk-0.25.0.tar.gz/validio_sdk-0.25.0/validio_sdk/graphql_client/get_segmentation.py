from typing import Optional

from .base_model import BaseModel
from .fragments import SegmentationDetails


class GetSegmentation(BaseModel):
    segmentation: Optional["GetSegmentationSegmentation"]


class GetSegmentationSegmentation(SegmentationDetails):
    pass


GetSegmentation.model_rebuild()

from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import SegmentationDetails


class ListSegmentations(BaseModel):
    segmentations_list: List["ListSegmentationsSegmentationsList"] = Field(
        alias="segmentationsList"
    )


class ListSegmentationsSegmentationsList(SegmentationDetails):
    pass


ListSegmentations.model_rebuild()

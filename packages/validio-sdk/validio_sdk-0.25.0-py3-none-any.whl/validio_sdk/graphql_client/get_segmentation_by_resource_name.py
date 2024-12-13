from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import SegmentationDetails


class GetSegmentationByResourceName(BaseModel):
    segmentation_by_resource_name: Optional[
        "GetSegmentationByResourceNameSegmentationByResourceName"
    ] = Field(alias="segmentationByResourceName")


class GetSegmentationByResourceNameSegmentationByResourceName(SegmentationDetails):
    pass


GetSegmentationByResourceName.model_rebuild()

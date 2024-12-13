from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import SegmentDetails


class SegmentsByResourceName(BaseModel):
    segments_by_resource_name: List["SegmentsByResourceNameSegmentsByResourceName"] = (
        Field(alias="segmentsByResourceName")
    )


class SegmentsByResourceNameSegmentsByResourceName(SegmentDetails):
    pass


SegmentsByResourceName.model_rebuild()

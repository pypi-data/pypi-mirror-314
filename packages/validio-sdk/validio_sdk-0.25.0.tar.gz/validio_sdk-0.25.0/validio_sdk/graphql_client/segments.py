from typing import List

from .base_model import BaseModel
from .fragments import SegmentDetails


class Segments(BaseModel):
    segments: List["SegmentsSegments"]


class SegmentsSegments(SegmentDetails):
    pass


Segments.model_rebuild()

from typing import List, Optional

from pydantic import Field

from validio_sdk.scalars import JsonPointer

from .base_model import BaseModel
from .fragments import SegmentationDetails


class GetSegmentsBySegmentation(BaseModel):
    segmentation: Optional["GetSegmentsBySegmentationSegmentation"]


class GetSegmentsBySegmentationSegmentation(SegmentationDetails):
    segments: "GetSegmentsBySegmentationSegmentationSegments"


class GetSegmentsBySegmentationSegmentationSegments(BaseModel):
    elements: List["GetSegmentsBySegmentationSegmentationSegmentsElements"]
    page_info: Optional["GetSegmentsBySegmentationSegmentationSegmentsPageInfo"] = (
        Field(alias="pageInfo")
    )


class GetSegmentsBySegmentationSegmentationSegmentsElements(BaseModel):
    fields: List["GetSegmentsBySegmentationSegmentationSegmentsElementsFields"]


class GetSegmentsBySegmentationSegmentationSegmentsElementsFields(BaseModel):
    field: JsonPointer
    value: str


class GetSegmentsBySegmentationSegmentationSegmentsPageInfo(BaseModel):
    start_cursor: Optional[str] = Field(alias="startCursor")
    end_cursor: Optional[str] = Field(alias="endCursor")
    has_next_page: Optional[bool] = Field(alias="hasNextPage")
    has_previous_page: Optional[bool] = Field(alias="hasPreviousPage")
    filtered_count: int = Field(alias="filteredCount")
    total_count: int = Field(alias="totalCount")


GetSegmentsBySegmentation.model_rebuild()
GetSegmentsBySegmentationSegmentation.model_rebuild()
GetSegmentsBySegmentationSegmentationSegments.model_rebuild()
GetSegmentsBySegmentationSegmentationSegmentsElements.model_rebuild()

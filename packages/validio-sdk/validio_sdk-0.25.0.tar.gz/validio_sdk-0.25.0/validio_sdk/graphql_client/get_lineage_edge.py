from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import LineageEdgeDetails


class GetLineageEdge(BaseModel):
    lineage_edge: Optional["GetLineageEdgeLineageEdge"] = Field(alias="lineageEdge")


class GetLineageEdgeLineageEdge(LineageEdgeDetails):
    pass


GetLineageEdge.model_rebuild()

from pydantic import Field

from .base_model import BaseModel
from .fragments import LineageEdgeCreation


class CreateLineageEdge(BaseModel):
    lineage_edge_create: "CreateLineageEdgeLineageEdgeCreate" = Field(
        alias="lineageEdgeCreate"
    )


class CreateLineageEdgeLineageEdgeCreate(LineageEdgeCreation):
    pass


CreateLineageEdge.model_rebuild()

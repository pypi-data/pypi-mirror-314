from pydantic import Field

from .base_model import BaseModel
from .fragments import LineageGraphDetails


class GetLineageGraph(BaseModel):
    lineage_graph: "GetLineageGraphLineageGraph" = Field(alias="lineageGraph")


class GetLineageGraphLineageGraph(LineageGraphDetails):
    pass


GetLineageGraph.model_rebuild()

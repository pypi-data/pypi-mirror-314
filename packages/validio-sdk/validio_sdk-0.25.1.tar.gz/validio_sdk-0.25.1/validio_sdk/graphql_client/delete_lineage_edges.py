from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteLineageEdges(BaseModel):
    lineage_edges_delete: "DeleteLineageEdgesLineageEdgesDelete" = Field(
        alias="lineageEdgesDelete"
    )


class DeleteLineageEdgesLineageEdgesDelete(BaseModel):
    errors: List["DeleteLineageEdgesLineageEdgesDeleteErrors"]


class DeleteLineageEdgesLineageEdgesDeleteErrors(ErrorDetails):
    pass


DeleteLineageEdges.model_rebuild()
DeleteLineageEdgesLineageEdgesDelete.model_rebuild()

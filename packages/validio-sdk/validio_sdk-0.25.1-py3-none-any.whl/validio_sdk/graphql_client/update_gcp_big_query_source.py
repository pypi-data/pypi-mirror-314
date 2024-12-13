from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateGcpBigQuerySource(BaseModel):
    gcp_big_query_source_update: "UpdateGcpBigQuerySourceGcpBigQuerySourceUpdate" = (
        Field(alias="gcpBigQuerySourceUpdate")
    )


class UpdateGcpBigQuerySourceGcpBigQuerySourceUpdate(SourceUpdate):
    pass


UpdateGcpBigQuerySource.model_rebuild()

from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateGcpPubSubLiteSource(BaseModel):
    gcp_pub_sub_lite_source_update: (
        "UpdateGcpPubSubLiteSourceGcpPubSubLiteSourceUpdate"
    ) = Field(alias="gcpPubSubLiteSourceUpdate")


class UpdateGcpPubSubLiteSourceGcpPubSubLiteSourceUpdate(SourceUpdate):
    pass


UpdateGcpPubSubLiteSource.model_rebuild()

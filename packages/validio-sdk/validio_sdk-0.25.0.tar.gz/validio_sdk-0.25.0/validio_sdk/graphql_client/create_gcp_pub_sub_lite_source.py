from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceCreation


class CreateGcpPubSubLiteSource(BaseModel):
    gcp_pub_sub_lite_source_create: (
        "CreateGcpPubSubLiteSourceGcpPubSubLiteSourceCreate"
    ) = Field(alias="gcpPubSubLiteSourceCreate")


class CreateGcpPubSubLiteSourceGcpPubSubLiteSourceCreate(SourceCreation):
    pass


CreateGcpPubSubLiteSource.model_rebuild()

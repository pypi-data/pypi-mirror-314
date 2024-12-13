from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceCreation


class CreateGcpPubSubSource(BaseModel):
    gcp_pub_sub_source_create: "CreateGcpPubSubSourceGcpPubSubSourceCreate" = Field(
        alias="gcpPubSubSourceCreate"
    )


class CreateGcpPubSubSourceGcpPubSubSourceCreate(SourceCreation):
    pass


CreateGcpPubSubSource.model_rebuild()

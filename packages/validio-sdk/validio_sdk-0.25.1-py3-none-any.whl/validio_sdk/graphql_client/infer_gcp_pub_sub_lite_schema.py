from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferGcpPubSubLiteSchema(BaseModel):
    gcp_pub_sub_lite_infer_schema: JsonTypeDefinition = Field(
        alias="gcpPubSubLiteInferSchema"
    )

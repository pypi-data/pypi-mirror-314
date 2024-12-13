from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferGcpPubSubSchema(BaseModel):
    gcp_pub_sub_infer_schema: JsonTypeDefinition = Field(alias="gcpPubSubInferSchema")

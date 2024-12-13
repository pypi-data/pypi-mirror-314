from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferGcpBigQuerySchema(BaseModel):
    gcp_big_query_infer_schema: JsonTypeDefinition = Field(
        alias="gcpBigQueryInferSchema"
    )

from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferSampleSchema(BaseModel):
    sample_infer_schema: JsonTypeDefinition = Field(alias="sampleInferSchema")

from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferDemoSchema(BaseModel):
    demo_infer_schema: JsonTypeDefinition = Field(alias="demoInferSchema")

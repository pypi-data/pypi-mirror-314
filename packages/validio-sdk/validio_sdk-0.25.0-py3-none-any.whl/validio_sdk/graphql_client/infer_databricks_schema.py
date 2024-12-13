from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferDatabricksSchema(BaseModel):
    databricks_infer_schema: JsonTypeDefinition = Field(alias="databricksInferSchema")

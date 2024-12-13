from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferDbtModelRunSchema(BaseModel):
    dbt_model_run_infer_schema: JsonTypeDefinition = Field(
        alias="dbtModelRunInferSchema"
    )

from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferDbtTestResultSchema(BaseModel):
    dbt_test_result_infer_schema: JsonTypeDefinition = Field(
        alias="dbtTestResultInferSchema"
    )

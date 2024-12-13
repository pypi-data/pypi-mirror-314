from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferPostgreSqlSchema(BaseModel):
    postgre_sql_infer_schema: JsonTypeDefinition = Field(alias="postgreSqlInferSchema")

from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferAwsAthenaSchema(BaseModel):
    aws_athena_infer_schema: JsonTypeDefinition = Field(alias="awsAthenaInferSchema")

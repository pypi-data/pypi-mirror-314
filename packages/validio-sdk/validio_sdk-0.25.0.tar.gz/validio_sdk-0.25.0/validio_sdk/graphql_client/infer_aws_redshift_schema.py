from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferAwsRedshiftSchema(BaseModel):
    aws_redshift_infer_schema: JsonTypeDefinition = Field(
        alias="awsRedshiftInferSchema"
    )

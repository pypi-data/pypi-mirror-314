from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferAwsS3Schema(BaseModel):
    aws_s3_infer_schema: JsonTypeDefinition = Field(alias="awsS3InferSchema")

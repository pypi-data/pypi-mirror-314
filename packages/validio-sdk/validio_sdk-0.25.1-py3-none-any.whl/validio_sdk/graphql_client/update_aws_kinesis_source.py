from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateAwsKinesisSource(BaseModel):
    aws_kinesis_source_update: "UpdateAwsKinesisSourceAwsKinesisSourceUpdate" = Field(
        alias="awsKinesisSourceUpdate"
    )


class UpdateAwsKinesisSourceAwsKinesisSourceUpdate(SourceUpdate):
    pass


UpdateAwsKinesisSource.model_rebuild()

from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateAwsS3Source(BaseModel):
    aws_s3_source_update: "UpdateAwsS3SourceAwsS3SourceUpdate" = Field(
        alias="awsS3SourceUpdate"
    )


class UpdateAwsS3SourceAwsS3SourceUpdate(SourceUpdate):
    pass


UpdateAwsS3Source.model_rebuild()

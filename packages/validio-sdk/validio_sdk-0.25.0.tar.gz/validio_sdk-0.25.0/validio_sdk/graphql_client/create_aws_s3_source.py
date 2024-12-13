from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceCreation


class CreateAwsS3Source(BaseModel):
    aws_s3_source_create: "CreateAwsS3SourceAwsS3SourceCreate" = Field(
        alias="awsS3SourceCreate"
    )


class CreateAwsS3SourceAwsS3SourceCreate(SourceCreation):
    pass


CreateAwsS3Source.model_rebuild()

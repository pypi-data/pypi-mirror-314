from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateAwsAthenaSource(BaseModel):
    aws_athena_source_update: "UpdateAwsAthenaSourceAwsAthenaSourceUpdate" = Field(
        alias="awsAthenaSourceUpdate"
    )


class UpdateAwsAthenaSourceAwsAthenaSourceUpdate(SourceUpdate):
    pass


UpdateAwsAthenaSource.model_rebuild()

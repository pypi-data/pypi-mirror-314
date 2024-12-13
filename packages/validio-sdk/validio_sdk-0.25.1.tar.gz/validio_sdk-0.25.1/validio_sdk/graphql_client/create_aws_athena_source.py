from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceCreation


class CreateAwsAthenaSource(BaseModel):
    aws_athena_source_create: "CreateAwsAthenaSourceAwsAthenaSourceCreate" = Field(
        alias="awsAthenaSourceCreate"
    )


class CreateAwsAthenaSourceAwsAthenaSourceCreate(SourceCreation):
    pass


CreateAwsAthenaSource.model_rebuild()

from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateAwsRedshiftSource(BaseModel):
    aws_redshift_source_update: "UpdateAwsRedshiftSourceAwsRedshiftSourceUpdate" = (
        Field(alias="awsRedshiftSourceUpdate")
    )


class UpdateAwsRedshiftSourceAwsRedshiftSourceUpdate(SourceUpdate):
    pass


UpdateAwsRedshiftSource.model_rebuild()

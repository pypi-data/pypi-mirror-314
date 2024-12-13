from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateSnowflakeSource(BaseModel):
    snowflake_source_update: "UpdateSnowflakeSourceSnowflakeSourceUpdate" = Field(
        alias="snowflakeSourceUpdate"
    )


class UpdateSnowflakeSourceSnowflakeSourceUpdate(SourceUpdate):
    pass


UpdateSnowflakeSource.model_rebuild()

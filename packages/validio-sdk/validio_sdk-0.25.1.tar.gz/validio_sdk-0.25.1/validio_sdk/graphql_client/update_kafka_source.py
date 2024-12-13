from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateKafkaSource(BaseModel):
    kafka_source_update: "UpdateKafkaSourceKafkaSourceUpdate" = Field(
        alias="kafkaSourceUpdate"
    )


class UpdateKafkaSourceKafkaSourceUpdate(SourceUpdate):
    pass


UpdateKafkaSource.model_rebuild()

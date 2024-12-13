from typing import Any, List

from pydantic import Field

from .base_model import BaseModel


class GetValidatorMetricDebugRecords(BaseModel):
    validator_metric_debug_records: (
        "GetValidatorMetricDebugRecordsValidatorMetricDebugRecords"
    ) = Field(alias="validatorMetricDebugRecords")


class GetValidatorMetricDebugRecordsValidatorMetricDebugRecords(BaseModel):
    columns: List[str]
    rows: List[Any]


GetValidatorMetricDebugRecords.model_rebuild()

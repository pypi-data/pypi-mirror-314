from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateFreshnessValidatorWithDynamicThreshold(BaseModel):
    freshness_validator_with_dynamic_threshold_create: (
        "CreateFreshnessValidatorWithDynamicThresholdFreshnessValidatorWithDynamicThresholdCreate"
    ) = Field(alias="freshnessValidatorWithDynamicThresholdCreate")


class CreateFreshnessValidatorWithDynamicThresholdFreshnessValidatorWithDynamicThresholdCreate(
    ValidatorCreation
):
    pass


CreateFreshnessValidatorWithDynamicThreshold.model_rebuild()

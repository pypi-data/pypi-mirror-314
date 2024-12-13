from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateFreshnessValidatorWithDifferenceThreshold(BaseModel):
    freshness_validator_with_difference_threshold_create: (
        "CreateFreshnessValidatorWithDifferenceThresholdFreshnessValidatorWithDifferenceThresholdCreate"
    ) = Field(alias="freshnessValidatorWithDifferenceThresholdCreate")


class CreateFreshnessValidatorWithDifferenceThresholdFreshnessValidatorWithDifferenceThresholdCreate(
    ValidatorCreation
):
    pass


CreateFreshnessValidatorWithDifferenceThreshold.model_rebuild()

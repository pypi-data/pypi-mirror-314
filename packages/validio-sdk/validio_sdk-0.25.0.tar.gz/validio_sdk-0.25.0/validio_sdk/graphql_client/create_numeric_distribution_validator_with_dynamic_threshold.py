from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateNumericDistributionValidatorWithDynamicThreshold(BaseModel):
    numeric_distribution_validator_with_dynamic_threshold_create: (
        "CreateNumericDistributionValidatorWithDynamicThresholdNumericDistributionValidatorWithDynamicThresholdCreate"
    ) = Field(alias="numericDistributionValidatorWithDynamicThresholdCreate")


class CreateNumericDistributionValidatorWithDynamicThresholdNumericDistributionValidatorWithDynamicThresholdCreate(
    ValidatorCreation
):
    pass


CreateNumericDistributionValidatorWithDynamicThreshold.model_rebuild()

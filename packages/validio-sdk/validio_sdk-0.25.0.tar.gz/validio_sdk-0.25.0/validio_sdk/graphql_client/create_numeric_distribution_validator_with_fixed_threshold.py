from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateNumericDistributionValidatorWithFixedThreshold(BaseModel):
    numeric_distribution_validator_with_fixed_threshold_create: (
        "CreateNumericDistributionValidatorWithFixedThresholdNumericDistributionValidatorWithFixedThresholdCreate"
    ) = Field(alias="numericDistributionValidatorWithFixedThresholdCreate")


class CreateNumericDistributionValidatorWithFixedThresholdNumericDistributionValidatorWithFixedThresholdCreate(
    ValidatorCreation
):
    pass


CreateNumericDistributionValidatorWithFixedThreshold.model_rebuild()

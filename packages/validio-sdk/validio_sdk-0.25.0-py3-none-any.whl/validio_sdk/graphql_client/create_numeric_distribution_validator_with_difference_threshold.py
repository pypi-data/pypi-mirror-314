from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateNumericDistributionValidatorWithDifferenceThreshold(BaseModel):
    numeric_distribution_validator_with_difference_threshold_create: (
        "CreateNumericDistributionValidatorWithDifferenceThresholdNumericDistributionValidatorWithDifferenceThresholdCreate"
    ) = Field(alias="numericDistributionValidatorWithDifferenceThresholdCreate")


class CreateNumericDistributionValidatorWithDifferenceThresholdNumericDistributionValidatorWithDifferenceThresholdCreate(
    ValidatorCreation
):
    pass


CreateNumericDistributionValidatorWithDifferenceThreshold.model_rebuild()

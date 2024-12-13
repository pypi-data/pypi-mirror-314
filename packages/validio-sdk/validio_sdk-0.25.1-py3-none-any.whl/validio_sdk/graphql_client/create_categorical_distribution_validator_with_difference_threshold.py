from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateCategoricalDistributionValidatorWithDifferenceThreshold(BaseModel):
    categorical_distribution_validator_with_difference_threshold_create: (
        "CreateCategoricalDistributionValidatorWithDifferenceThresholdCategoricalDistributionValidatorWithDifferenceThresholdCreate"
    ) = Field(alias="categoricalDistributionValidatorWithDifferenceThresholdCreate")


class CreateCategoricalDistributionValidatorWithDifferenceThresholdCategoricalDistributionValidatorWithDifferenceThresholdCreate(
    ValidatorCreation
):
    pass


CreateCategoricalDistributionValidatorWithDifferenceThreshold.model_rebuild()

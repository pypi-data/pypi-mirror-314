from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateCategoricalDistributionValidatorWithFixedThreshold(BaseModel):
    categorical_distribution_validator_with_fixed_threshold_create: (
        "CreateCategoricalDistributionValidatorWithFixedThresholdCategoricalDistributionValidatorWithFixedThresholdCreate"
    ) = Field(alias="categoricalDistributionValidatorWithFixedThresholdCreate")


class CreateCategoricalDistributionValidatorWithFixedThresholdCategoricalDistributionValidatorWithFixedThresholdCreate(
    ValidatorCreation
):
    pass


CreateCategoricalDistributionValidatorWithFixedThreshold.model_rebuild()

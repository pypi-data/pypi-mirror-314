from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateCategoricalDistributionValidatorWithDynamicThreshold(BaseModel):
    categorical_distribution_validator_with_dynamic_threshold_create: (
        "CreateCategoricalDistributionValidatorWithDynamicThresholdCategoricalDistributionValidatorWithDynamicThresholdCreate"
    ) = Field(alias="categoricalDistributionValidatorWithDynamicThresholdCreate")


class CreateCategoricalDistributionValidatorWithDynamicThresholdCategoricalDistributionValidatorWithDynamicThresholdCreate(
    ValidatorCreation
):
    pass


CreateCategoricalDistributionValidatorWithDynamicThreshold.model_rebuild()

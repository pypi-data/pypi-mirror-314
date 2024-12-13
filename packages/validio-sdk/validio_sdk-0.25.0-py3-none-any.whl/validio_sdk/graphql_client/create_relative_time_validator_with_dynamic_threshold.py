from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateRelativeTimeValidatorWithDynamicThreshold(BaseModel):
    relative_time_validator_with_dynamic_threshold_create: (
        "CreateRelativeTimeValidatorWithDynamicThresholdRelativeTimeValidatorWithDynamicThresholdCreate"
    ) = Field(alias="relativeTimeValidatorWithDynamicThresholdCreate")


class CreateRelativeTimeValidatorWithDynamicThresholdRelativeTimeValidatorWithDynamicThresholdCreate(
    ValidatorCreation
):
    pass


CreateRelativeTimeValidatorWithDynamicThreshold.model_rebuild()

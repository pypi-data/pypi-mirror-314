from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateRelativeTimeValidatorWithDifferenceThreshold(BaseModel):
    relative_time_validator_with_difference_threshold_create: (
        "CreateRelativeTimeValidatorWithDifferenceThresholdRelativeTimeValidatorWithDifferenceThresholdCreate"
    ) = Field(alias="relativeTimeValidatorWithDifferenceThresholdCreate")


class CreateRelativeTimeValidatorWithDifferenceThresholdRelativeTimeValidatorWithDifferenceThresholdCreate(
    ValidatorCreation
):
    pass


CreateRelativeTimeValidatorWithDifferenceThreshold.model_rebuild()

from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateRelativeVolumeValidatorWithDifferenceThreshold(BaseModel):
    relative_volume_validator_with_difference_threshold_create: (
        "CreateRelativeVolumeValidatorWithDifferenceThresholdRelativeVolumeValidatorWithDifferenceThresholdCreate"
    ) = Field(alias="relativeVolumeValidatorWithDifferenceThresholdCreate")


class CreateRelativeVolumeValidatorWithDifferenceThresholdRelativeVolumeValidatorWithDifferenceThresholdCreate(
    ValidatorCreation
):
    pass


CreateRelativeVolumeValidatorWithDifferenceThreshold.model_rebuild()

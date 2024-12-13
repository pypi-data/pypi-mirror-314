from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateVolumeValidatorWithDifferenceThreshold(BaseModel):
    volume_validator_with_difference_threshold_create: (
        "CreateVolumeValidatorWithDifferenceThresholdVolumeValidatorWithDifferenceThresholdCreate"
    ) = Field(alias="volumeValidatorWithDifferenceThresholdCreate")


class CreateVolumeValidatorWithDifferenceThresholdVolumeValidatorWithDifferenceThresholdCreate(
    ValidatorCreation
):
    pass


CreateVolumeValidatorWithDifferenceThreshold.model_rebuild()

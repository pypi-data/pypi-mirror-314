from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateVolumeValidatorWithFixedThreshold(BaseModel):
    volume_validator_with_fixed_threshold_create: (
        "CreateVolumeValidatorWithFixedThresholdVolumeValidatorWithFixedThresholdCreate"
    ) = Field(alias="volumeValidatorWithFixedThresholdCreate")


class CreateVolumeValidatorWithFixedThresholdVolumeValidatorWithFixedThresholdCreate(
    ValidatorCreation
):
    pass


CreateVolumeValidatorWithFixedThreshold.model_rebuild()

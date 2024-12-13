from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateVolumeValidatorWithDynamicThreshold(BaseModel):
    volume_validator_with_dynamic_threshold_create: (
        "CreateVolumeValidatorWithDynamicThresholdVolumeValidatorWithDynamicThresholdCreate"
    ) = Field(alias="volumeValidatorWithDynamicThresholdCreate")


class CreateVolumeValidatorWithDynamicThresholdVolumeValidatorWithDynamicThresholdCreate(
    ValidatorCreation
):
    pass


CreateVolumeValidatorWithDynamicThreshold.model_rebuild()

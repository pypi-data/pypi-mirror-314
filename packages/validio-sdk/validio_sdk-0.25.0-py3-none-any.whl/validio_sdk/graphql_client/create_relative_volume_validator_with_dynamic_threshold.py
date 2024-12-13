from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateRelativeVolumeValidatorWithDynamicThreshold(BaseModel):
    relative_volume_validator_with_dynamic_threshold_create: (
        "CreateRelativeVolumeValidatorWithDynamicThresholdRelativeVolumeValidatorWithDynamicThresholdCreate"
    ) = Field(alias="relativeVolumeValidatorWithDynamicThresholdCreate")


class CreateRelativeVolumeValidatorWithDynamicThresholdRelativeVolumeValidatorWithDynamicThresholdCreate(
    ValidatorCreation
):
    pass


CreateRelativeVolumeValidatorWithDynamicThreshold.model_rebuild()

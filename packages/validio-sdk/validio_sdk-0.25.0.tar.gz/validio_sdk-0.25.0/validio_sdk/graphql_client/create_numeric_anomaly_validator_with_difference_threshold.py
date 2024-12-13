from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateNumericAnomalyValidatorWithDifferenceThreshold(BaseModel):
    numeric_anomaly_validator_with_difference_threshold_create: (
        "CreateNumericAnomalyValidatorWithDifferenceThresholdNumericAnomalyValidatorWithDifferenceThresholdCreate"
    ) = Field(alias="numericAnomalyValidatorWithDifferenceThresholdCreate")


class CreateNumericAnomalyValidatorWithDifferenceThresholdNumericAnomalyValidatorWithDifferenceThresholdCreate(
    ValidatorCreation
):
    pass


CreateNumericAnomalyValidatorWithDifferenceThreshold.model_rebuild()

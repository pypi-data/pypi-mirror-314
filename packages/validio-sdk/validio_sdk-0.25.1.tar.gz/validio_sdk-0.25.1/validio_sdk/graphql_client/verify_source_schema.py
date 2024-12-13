from typing import List, Literal

from pydantic import Field

from validio_sdk.scalars import JsonPointer, SegmentationId, ValidatorId, WindowId

from .base_model import BaseModel


class VerifySourceSchema(BaseModel):
    source_schema_verify: "VerifySourceSchemaSourceSchemaVerify" = Field(
        alias="sourceSchemaVerify"
    )


class VerifySourceSchemaSourceSchemaVerify(BaseModel):
    validator_conflicts: List[
        "VerifySourceSchemaSourceSchemaVerifyValidatorConflicts"
    ] = Field(alias="validatorConflicts")
    segmentation_conflicts: List[
        "VerifySourceSchemaSourceSchemaVerifySegmentationConflicts"
    ] = Field(alias="segmentationConflicts")
    window_conflicts: List["VerifySourceSchemaSourceSchemaVerifyWindowConflicts"] = (
        Field(alias="windowConflicts")
    )


class VerifySourceSchemaSourceSchemaVerifyValidatorConflicts(BaseModel):
    validator: "VerifySourceSchemaSourceSchemaVerifyValidatorConflictsValidator"
    fields: List[JsonPointer]


class VerifySourceSchemaSourceSchemaVerifyValidatorConflictsValidator(BaseModel):
    typename__: Literal[
        "CategoricalDistributionValidator",
        "FreshnessValidator",
        "NumericAnomalyValidator",
        "NumericDistributionValidator",
        "NumericValidator",
        "RelativeTimeValidator",
        "RelativeVolumeValidator",
        "SqlValidator",
        "Validator",
        "VolumeValidator",
    ] = Field(alias="__typename")
    id: ValidatorId
    name: str


class VerifySourceSchemaSourceSchemaVerifySegmentationConflicts(BaseModel):
    segmentation: (
        "VerifySourceSchemaSourceSchemaVerifySegmentationConflictsSegmentation"
    )
    fields: List[JsonPointer]


class VerifySourceSchemaSourceSchemaVerifySegmentationConflictsSegmentation(BaseModel):
    id: SegmentationId
    name: str


class VerifySourceSchemaSourceSchemaVerifyWindowConflicts(BaseModel):
    window: "VerifySourceSchemaSourceSchemaVerifyWindowConflictsWindow"
    fields: List[JsonPointer]


class VerifySourceSchemaSourceSchemaVerifyWindowConflictsWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str


VerifySourceSchema.model_rebuild()
VerifySourceSchemaSourceSchemaVerify.model_rebuild()
VerifySourceSchemaSourceSchemaVerifyValidatorConflicts.model_rebuild()
VerifySourceSchemaSourceSchemaVerifySegmentationConflicts.model_rebuild()
VerifySourceSchemaSourceSchemaVerifyWindowConflicts.model_rebuild()

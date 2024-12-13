from datetime import datetime
from typing import List, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel
from .enums import ComparisonOperator, DecisionBoundsType, IncidentSeverity


class GetValidatorSegmentMetrics(BaseModel):
    validator_segment_metrics: Union[
        "GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithDifferenceThresholdHistory",
        "GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithDynamicThresholdHistory",
        "GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithFixedThresholdHistory",
    ] = Field(alias="validatorSegmentMetrics", discriminator="typename__")


class GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithDifferenceThresholdHistory(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithDifferenceThresholdHistory"] = Field(
        alias="__typename"
    )
    values: List[
        "GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithDifferenceThresholdHistoryValues"
    ]


class GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithDifferenceThresholdHistoryValues(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithDifferenceThreshold"] = Field(
        alias="__typename"
    )
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float
    severity: Optional[IncidentSeverity]
    deviation: float
    lower_bound: Optional[float] = Field(alias="maybeLowerBound")
    upper_bound: Optional[float] = Field(alias="maybeUpperBound")


class GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithDynamicThresholdHistory(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithDynamicThresholdHistory"] = Field(
        alias="__typename"
    )
    values: List[
        "GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithDynamicThresholdHistoryValues"
    ]


class GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithDynamicThresholdHistoryValues(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithDynamicThreshold"] = Field(
        alias="__typename"
    )
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float
    severity: Optional[IncidentSeverity]
    deviation: float
    lower_bound: float = Field(alias="lowerBound")
    upper_bound: float = Field(alias="upperBound")
    decision_bounds_type: DecisionBoundsType = Field(alias="decisionBoundsType")
    is_burn_in: bool = Field(alias="isBurnIn")


class GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithFixedThresholdHistory(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithFixedThresholdHistory"] = Field(
        alias="__typename"
    )
    values: List[
        "GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithFixedThresholdHistoryValues"
    ]


class GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithFixedThresholdHistoryValues(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithFixedThreshold"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float
    severity: Optional[IncidentSeverity]
    deviation: float
    operator: ComparisonOperator
    bound: float


GetValidatorSegmentMetrics.model_rebuild()
GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithDifferenceThresholdHistory.model_rebuild()
GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithDynamicThresholdHistory.model_rebuild()
GetValidatorSegmentMetricsValidatorSegmentMetricsValidatorMetricWithFixedThresholdHistory.model_rebuild()

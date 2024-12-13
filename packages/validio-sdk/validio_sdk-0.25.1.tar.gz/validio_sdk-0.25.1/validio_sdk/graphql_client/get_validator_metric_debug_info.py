from datetime import datetime
from typing import List, Literal, Union

from pydantic import Field

from .base_model import BaseModel


class GetValidatorMetricDebugInfo(BaseModel):
    validator_metric_debug_info: Union[
        "GetValidatorMetricDebugInfoValidatorMetricDebugInfoValidatorMetricDebugInfo",
        "GetValidatorMetricDebugInfoValidatorMetricDebugInfoAwsAthenaSourceDebugInfo",
        "GetValidatorMetricDebugInfoValidatorMetricDebugInfoAwsRedShiftSourceDebugInfo",
        "GetValidatorMetricDebugInfoValidatorMetricDebugInfoAwsS3SourceDebugInfo",
        "GetValidatorMetricDebugInfoValidatorMetricDebugInfoAzureSynapseSourceDebugInfo",
        "GetValidatorMetricDebugInfoValidatorMetricDebugInfoClickHouseSourceDebugInfo",
        "GetValidatorMetricDebugInfoValidatorMetricDebugInfoDatabricksSourceDebugInfo",
        "GetValidatorMetricDebugInfoValidatorMetricDebugInfoGcpBigQuerySourceDebugInfo",
        "GetValidatorMetricDebugInfoValidatorMetricDebugInfoGcpStorageSourceDebugInfo",
        "GetValidatorMetricDebugInfoValidatorMetricDebugInfoPostgreSQLSourceDebugInfo",
        "GetValidatorMetricDebugInfoValidatorMetricDebugInfoSnowflakeSourceDebugInfo",
    ] = Field(alias="validatorMetricDebugInfo", discriminator="typename__")


class GetValidatorMetricDebugInfoValidatorMetricDebugInfoValidatorMetricDebugInfo(
    BaseModel
):
    typename__: Literal["ValidatorMetricDebugInfo"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")


class GetValidatorMetricDebugInfoValidatorMetricDebugInfoAwsAthenaSourceDebugInfo(
    BaseModel
):
    typename__: Literal["AwsAthenaSourceDebugInfo"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    sql_query: str = Field(alias="sqlQuery")


class GetValidatorMetricDebugInfoValidatorMetricDebugInfoAwsRedShiftSourceDebugInfo(
    BaseModel
):
    typename__: Literal["AwsRedShiftSourceDebugInfo"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    sql_query: str = Field(alias="sqlQuery")


class GetValidatorMetricDebugInfoValidatorMetricDebugInfoAwsS3SourceDebugInfo(
    BaseModel
):
    typename__: Literal["AwsS3SourceDebugInfo"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    bucket: str
    file_path: List[str] = Field(alias="filePath")


class GetValidatorMetricDebugInfoValidatorMetricDebugInfoAzureSynapseSourceDebugInfo(
    BaseModel
):
    typename__: Literal["AzureSynapseSourceDebugInfo"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    sql_query: str = Field(alias="sqlQuery")


class GetValidatorMetricDebugInfoValidatorMetricDebugInfoClickHouseSourceDebugInfo(
    BaseModel
):
    typename__: Literal["ClickHouseSourceDebugInfo"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    sql_query: str = Field(alias="sqlQuery")


class GetValidatorMetricDebugInfoValidatorMetricDebugInfoDatabricksSourceDebugInfo(
    BaseModel
):
    typename__: Literal["DatabricksSourceDebugInfo"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    sql_query: str = Field(alias="sqlQuery")


class GetValidatorMetricDebugInfoValidatorMetricDebugInfoGcpBigQuerySourceDebugInfo(
    BaseModel
):
    typename__: Literal["GcpBigQuerySourceDebugInfo"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    sql_query: str = Field(alias="sqlQuery")


class GetValidatorMetricDebugInfoValidatorMetricDebugInfoGcpStorageSourceDebugInfo(
    BaseModel
):
    typename__: Literal["GcpStorageSourceDebugInfo"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    bucket: str
    file_path: List[str] = Field(alias="filePath")


class GetValidatorMetricDebugInfoValidatorMetricDebugInfoPostgreSQLSourceDebugInfo(
    BaseModel
):
    typename__: Literal["PostgreSQLSourceDebugInfo"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    sql_query: str = Field(alias="sqlQuery")


class GetValidatorMetricDebugInfoValidatorMetricDebugInfoSnowflakeSourceDebugInfo(
    BaseModel
):
    typename__: Literal["SnowflakeSourceDebugInfo"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    sql_query: str = Field(alias="sqlQuery")


GetValidatorMetricDebugInfo.model_rebuild()

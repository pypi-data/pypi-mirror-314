from datetime import datetime
from typing import Any, List, Literal, Optional

from pydantic import Field

from validio_sdk.scalars import JsonPointer, SourceId, ValidatorId

from .base_model import BaseModel
from .enums import IncidentGroupPriority, IncidentRelationship, IncidentStatus


class GetIncidentRelatedGroups(BaseModel):
    incident_related_groups: "GetIncidentRelatedGroupsIncidentRelatedGroups" = Field(
        alias="incidentRelatedGroups"
    )


class GetIncidentRelatedGroupsIncidentRelatedGroups(BaseModel):
    origin_field: Optional[str] = Field(alias="originField")
    origin_fields: Optional[List[str]] = Field(alias="originFields")
    elements: List["GetIncidentRelatedGroupsIncidentRelatedGroupsElements"]


class GetIncidentRelatedGroupsIncidentRelatedGroupsElements(BaseModel):
    group: "GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroup"
    field: Optional[str]
    origin_field: Optional[str] = Field(alias="originField")
    relationship: IncidentRelationship


class GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroup(BaseModel):
    id: Any
    status: IncidentStatus
    priority: IncidentGroupPriority
    owner: Optional["GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupOwner"]
    source: "GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupSource"
    validator: "GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupValidator"
    segment: "GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupSegment"
    severity_stats: (
        "GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupSeverityStats"
    ) = Field(alias="severityStats")
    first_seen_at: datetime = Field(alias="firstSeenAt")
    last_seen_at: datetime = Field(alias="lastSeenAt")


class GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupOwner(BaseModel):
    id: Any
    display_name: str = Field(alias="displayName")


class GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    catalog_asset: Optional[
        "GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    name: str


class GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupSourceCatalogAsset(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "MsPowerBiDataflowCatalogAsset",
        "MsPowerBiReportCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any


class GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupValidator(BaseModel):
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


class GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupSegment(BaseModel):
    fields: List[
        "GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupSegmentFields"
    ]


class GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupSegmentFields(
    BaseModel
):
    field: JsonPointer
    value: str


class GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupSeverityStats(
    BaseModel
):
    high_count: int = Field(alias="highCount")
    medium_count: int = Field(alias="mediumCount")
    low_count: int = Field(alias="lowCount")
    total_count: int = Field(alias="totalCount")


GetIncidentRelatedGroups.model_rebuild()
GetIncidentRelatedGroupsIncidentRelatedGroups.model_rebuild()
GetIncidentRelatedGroupsIncidentRelatedGroupsElements.model_rebuild()
GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroup.model_rebuild()
GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupSource.model_rebuild()
GetIncidentRelatedGroupsIncidentRelatedGroupsElementsGroupSegment.model_rebuild()

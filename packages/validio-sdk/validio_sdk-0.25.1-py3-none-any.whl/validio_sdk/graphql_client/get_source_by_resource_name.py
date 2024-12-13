from datetime import datetime
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import (
    CredentialId,
    CronExpression,
    JsonTypeDefinition,
    SegmentationId,
    SourceId,
    WindowId,
)

from .base_model import BaseModel
from .enums import (
    CatalogAssetType,
    FileFormat,
    SourceState,
    StreamingSourceMessageFormat,
)


class GetSourceByResourceName(BaseModel):
    source_by_resource_name: Optional[
        Annotated[
            Union[
                "GetSourceByResourceNameSourceByResourceNameSource",
                "GetSourceByResourceNameSourceByResourceNameAwsAthenaSource",
                "GetSourceByResourceNameSourceByResourceNameAwsKinesisSource",
                "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSource",
                "GetSourceByResourceNameSourceByResourceNameAwsS3Source",
                "GetSourceByResourceNameSourceByResourceNameAzureSynapseSource",
                "GetSourceByResourceNameSourceByResourceNameClickHouseSource",
                "GetSourceByResourceNameSourceByResourceNameDatabricksSource",
                "GetSourceByResourceNameSourceByResourceNameDbtModelRunSource",
                "GetSourceByResourceNameSourceByResourceNameDbtTestResultSource",
                "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySource",
                "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSource",
                "GetSourceByResourceNameSourceByResourceNameGcpPubSubSource",
                "GetSourceByResourceNameSourceByResourceNameGcpStorageSource",
                "GetSourceByResourceNameSourceByResourceNameKafkaSource",
                "GetSourceByResourceNameSourceByResourceNamePostgreSqlSource",
                "GetSourceByResourceNameSourceByResourceNameSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceByResourceName")


class GetSourceByResourceNameSourceByResourceNameSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameSourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameSourceFilters"]


class GetSourceByResourceNameSourceByResourceNameSourceCatalogAsset(BaseModel):
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
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameSourceCredentialNamespace"


class GetSourceByResourceNameSourceByResourceNameSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameSourceWindowsNamespace"


class GetSourceByResourceNameSourceByResourceNameSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameSourceFiltersNamespace"


class GetSourceByResourceNameSourceByResourceNameSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceConfig"


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsAthenaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceCredentialNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceConfig(BaseModel):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceConfig"


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["AwsKinesisCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceCredentialNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceConfig(BaseModel):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional[
        "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceConfig"


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["AwsRedshiftCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceCredentialNamespace"


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameAwsS3SourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameAwsS3SourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameAwsS3SourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameAwsS3SourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAwsS3SourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameAwsS3SourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameAwsS3SourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNameAwsS3SourceConfig"


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceCatalogAsset(BaseModel):
    typename__: Literal["AwsS3CatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameAwsS3SourceCredentialNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAwsS3SourceWindowsNamespace"


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameAwsS3SourceSegmentationsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAwsS3SourceFiltersNamespace"


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional["GetSourceByResourceNameSourceByResourceNameAwsS3SourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSource(BaseModel):
    typename__: Literal["AzureSynapseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: (
        "GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceTags"]
    filters: List[
        "GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceFilters"
    ]
    config: "GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceConfig"


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceCredentialNamespace"


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameClickHouseSource(BaseModel):
    typename__: Literal["ClickHouseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameClickHouseSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameClickHouseSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameClickHouseSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameClickHouseSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameClickHouseSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameClickHouseSourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameClickHouseSourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNameClickHouseSourceConfig"


class GetSourceByResourceNameSourceByResourceNameClickHouseSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["ClickHouseCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameClickHouseSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameClickHouseSourceCredentialNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameClickHouseSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameClickHouseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameClickHouseSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameClickHouseSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameClickHouseSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameClickHouseSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameClickHouseSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameClickHouseSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameClickHouseSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameClickHouseSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameClickHouseSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameClickHouseSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameClickHouseSourceConfig(BaseModel):
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameDatabricksSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameDatabricksSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameDatabricksSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameDatabricksSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameDatabricksSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameDatabricksSourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameDatabricksSourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNameDatabricksSourceConfig"


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["DatabricksCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameDatabricksSourceCredentialNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameDatabricksSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameDatabricksSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameDatabricksSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceConfig(BaseModel):
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]
    http_path: Optional[str] = Field(alias="httpPath")


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSource(BaseModel):
    typename__: Literal["DbtModelRunSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceConfig"


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceCatalogAsset(
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
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceCredentialNamespace"


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSource(BaseModel):
    typename__: Literal["DbtTestResultSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: (
        "GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceTags"]
    filters: List[
        "GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceFilters"
    ]
    config: "GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceConfig"


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceCatalogAsset(
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
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceCredentialNamespace"


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceConfig"


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceCatalogAsset(
    BaseModel
):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceCredentialNamespace"


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceConfig(BaseModel):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSource(BaseModel):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: (
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceTags"]
    filters: List[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceFilters"
    ]
    config: "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceConfig"


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["GcpPubSubLiteCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceCredentialNamespace"


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceConfig(BaseModel):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceConfig"


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceCredentialNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceConfig(BaseModel):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameSourceByResourceNameGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameGcpStorageSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameGcpStorageSourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameGcpStorageSourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceConfig"


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["GcpStorageCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceCredentialNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceConfig(BaseModel):
    project: str
    bucket: str
    folder: str
    csv: Optional[
        "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceConfigCsv"
    ]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceByResourceNameSourceByResourceNameKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameKafkaSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameKafkaSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameKafkaSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameKafkaSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameKafkaSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameKafkaSourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameKafkaSourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNameKafkaSourceConfig"


class GetSourceByResourceNameSourceByResourceNameKafkaSourceCatalogAsset(BaseModel):
    typename__: Literal["KafkaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameKafkaSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameKafkaSourceCredentialNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameKafkaSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameKafkaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameKafkaSourceWindowsNamespace"


class GetSourceByResourceNameSourceByResourceNameKafkaSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameKafkaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameKafkaSourceSegmentationsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameKafkaSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameKafkaSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameKafkaSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameKafkaSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameKafkaSourceFiltersNamespace"


class GetSourceByResourceNameSourceByResourceNameKafkaSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional[
        "GetSourceByResourceNameSourceByResourceNameKafkaSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameSourceByResourceNameKafkaSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceConfig"


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["PostgreSqlCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceCredentialNamespace"
    )


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameSourceByResourceNameSnowflakeSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameSourceByResourceNameSnowflakeSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameSnowflakeSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameSnowflakeSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameSnowflakeSourceNamespace"
    tags: List["GetSourceByResourceNameSourceByResourceNameSnowflakeSourceTags"]
    filters: List["GetSourceByResourceNameSourceByResourceNameSnowflakeSourceFilters"]
    config: "GetSourceByResourceNameSourceByResourceNameSnowflakeSourceConfig"


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceCatalogAsset(BaseModel):
    typename__: Literal["SnowflakeCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "MsPowerBiCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameSnowflakeSourceCredentialNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameSnowflakeSourceWindowsNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameSourceByResourceNameSnowflakeSourceSegmentationsNamespace"


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceFilters(BaseModel):
    typename__: Literal[
        "BooleanFilter",
        "EnumFilter",
        "Filter",
        "NullFilter",
        "SqlFilter",
        "StringFilter",
        "ThresholdFilter",
    ] = Field(alias="__typename")
    id: Any
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameSourceByResourceNameSnowflakeSourceFiltersNamespace"
    )


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceConfig(BaseModel):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


GetSourceByResourceName.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsAthenaSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsKinesisSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsRedshiftSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsS3Source.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsS3SourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsS3SourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsS3SourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsS3SourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsS3SourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAzureSynapseSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAzureSynapseSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameClickHouseSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameClickHouseSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameClickHouseSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameClickHouseSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameClickHouseSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDatabricksSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDatabricksSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDatabricksSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDatabricksSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDatabricksSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDbtModelRunSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDbtModelRunSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDbtTestResultSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDbtTestResultSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpBigQuerySource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpStorageSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpStorageSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpStorageSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpStorageSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpStorageSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpStorageSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameKafkaSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameKafkaSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameKafkaSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameKafkaSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameKafkaSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameKafkaSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNamePostgreSqlSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceFilters.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSnowflakeSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSnowflakeSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSnowflakeSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSnowflakeSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSnowflakeSourceFilters.model_rebuild()

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


class GetSource(BaseModel):
    source: Optional[
        Annotated[
            Union[
                "GetSourceSourceSource",
                "GetSourceSourceAwsAthenaSource",
                "GetSourceSourceAwsKinesisSource",
                "GetSourceSourceAwsRedshiftSource",
                "GetSourceSourceAwsS3Source",
                "GetSourceSourceAzureSynapseSource",
                "GetSourceSourceClickHouseSource",
                "GetSourceSourceDatabricksSource",
                "GetSourceSourceDbtModelRunSource",
                "GetSourceSourceDbtTestResultSource",
                "GetSourceSourceGcpBigQuerySource",
                "GetSourceSourceGcpPubSubLiteSource",
                "GetSourceSourceGcpPubSubSource",
                "GetSourceSourceGcpStorageSource",
                "GetSourceSourceKafkaSource",
                "GetSourceSourcePostgreSqlSource",
                "GetSourceSourceSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetSourceSourceSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceSourceCredential"
    windows: List["GetSourceSourceSourceWindows"]
    segmentations: List["GetSourceSourceSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceSourceNamespace"
    tags: List["GetSourceSourceSourceTags"]
    filters: List["GetSourceSourceSourceFilters"]


class GetSourceSourceSourceCatalogAsset(BaseModel):
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


class GetSourceSourceSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceSourceCredentialNamespace"


class GetSourceSourceSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceSourceWindowsNamespace"


class GetSourceSourceSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceSourceSegmentationsNamespace"


class GetSourceSourceSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceSourceFiltersNamespace"


class GetSourceSourceSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceAwsAthenaSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceAwsAthenaSourceCredential"
    windows: List["GetSourceSourceAwsAthenaSourceWindows"]
    segmentations: List["GetSourceSourceAwsAthenaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAwsAthenaSourceNamespace"
    tags: List["GetSourceSourceAwsAthenaSourceTags"]
    filters: List["GetSourceSourceAwsAthenaSourceFilters"]
    config: "GetSourceSourceAwsAthenaSourceConfig"


class GetSourceSourceAwsAthenaSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsAthenaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceAwsAthenaSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceAwsAthenaSourceCredentialNamespace"


class GetSourceSourceAwsAthenaSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsAthenaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAwsAthenaSourceWindowsNamespace"


class GetSourceSourceAwsAthenaSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsAthenaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAwsAthenaSourceSegmentationsNamespace"


class GetSourceSourceAwsAthenaSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsAthenaSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsAthenaSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceAwsAthenaSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceAwsAthenaSourceFiltersNamespace"


class GetSourceSourceAwsAthenaSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsAthenaSourceConfig(BaseModel):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceSourceAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceAwsKinesisSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceAwsKinesisSourceCredential"
    windows: List["GetSourceSourceAwsKinesisSourceWindows"]
    segmentations: List["GetSourceSourceAwsKinesisSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAwsKinesisSourceNamespace"
    tags: List["GetSourceSourceAwsKinesisSourceTags"]
    filters: List["GetSourceSourceAwsKinesisSourceFilters"]
    config: "GetSourceSourceAwsKinesisSourceConfig"


class GetSourceSourceAwsKinesisSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsKinesisCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceAwsKinesisSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceAwsKinesisSourceCredentialNamespace"


class GetSourceSourceAwsKinesisSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsKinesisSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAwsKinesisSourceWindowsNamespace"


class GetSourceSourceAwsKinesisSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsKinesisSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAwsKinesisSourceSegmentationsNamespace"


class GetSourceSourceAwsKinesisSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsKinesisSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsKinesisSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceAwsKinesisSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceAwsKinesisSourceFiltersNamespace"


class GetSourceSourceAwsKinesisSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsKinesisSourceConfig(BaseModel):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional["GetSourceSourceAwsKinesisSourceConfigMessageFormat"] = (
        Field(alias="messageFormat")
    )


class GetSourceSourceAwsKinesisSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceSourceAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceAwsRedshiftSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceAwsRedshiftSourceCredential"
    windows: List["GetSourceSourceAwsRedshiftSourceWindows"]
    segmentations: List["GetSourceSourceAwsRedshiftSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAwsRedshiftSourceNamespace"
    tags: List["GetSourceSourceAwsRedshiftSourceTags"]
    filters: List["GetSourceSourceAwsRedshiftSourceFilters"]
    config: "GetSourceSourceAwsRedshiftSourceConfig"


class GetSourceSourceAwsRedshiftSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsRedshiftCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceAwsRedshiftSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceAwsRedshiftSourceCredentialNamespace"


class GetSourceSourceAwsRedshiftSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsRedshiftSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAwsRedshiftSourceWindowsNamespace"


class GetSourceSourceAwsRedshiftSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsRedshiftSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAwsRedshiftSourceSegmentationsNamespace"


class GetSourceSourceAwsRedshiftSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsRedshiftSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsRedshiftSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceAwsRedshiftSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceAwsRedshiftSourceFiltersNamespace"


class GetSourceSourceAwsRedshiftSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsRedshiftSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceSourceAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceAwsS3SourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceAwsS3SourceCredential"
    windows: List["GetSourceSourceAwsS3SourceWindows"]
    segmentations: List["GetSourceSourceAwsS3SourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAwsS3SourceNamespace"
    tags: List["GetSourceSourceAwsS3SourceTags"]
    filters: List["GetSourceSourceAwsS3SourceFilters"]
    config: "GetSourceSourceAwsS3SourceConfig"


class GetSourceSourceAwsS3SourceCatalogAsset(BaseModel):
    typename__: Literal["AwsS3CatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceAwsS3SourceCredential(BaseModel):
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
    namespace: "GetSourceSourceAwsS3SourceCredentialNamespace"


class GetSourceSourceAwsS3SourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsS3SourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAwsS3SourceWindowsNamespace"


class GetSourceSourceAwsS3SourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsS3SourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAwsS3SourceSegmentationsNamespace"


class GetSourceSourceAwsS3SourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsS3SourceNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsS3SourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceAwsS3SourceFilters(BaseModel):
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
    namespace: "GetSourceSourceAwsS3SourceFiltersNamespace"


class GetSourceSourceAwsS3SourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional["GetSourceSourceAwsS3SourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceSourceAwsS3SourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceSourceAzureSynapseSource(BaseModel):
    typename__: Literal["AzureSynapseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceAzureSynapseSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceAzureSynapseSourceCredential"
    windows: List["GetSourceSourceAzureSynapseSourceWindows"]
    segmentations: List["GetSourceSourceAzureSynapseSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAzureSynapseSourceNamespace"
    tags: List["GetSourceSourceAzureSynapseSourceTags"]
    filters: List["GetSourceSourceAzureSynapseSourceFilters"]
    config: "GetSourceSourceAzureSynapseSourceConfig"


class GetSourceSourceAzureSynapseSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceAzureSynapseSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceAzureSynapseSourceCredentialNamespace"


class GetSourceSourceAzureSynapseSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceAzureSynapseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAzureSynapseSourceWindowsNamespace"


class GetSourceSourceAzureSynapseSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceAzureSynapseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceAzureSynapseSourceSegmentationsNamespace"


class GetSourceSourceAzureSynapseSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceAzureSynapseSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceAzureSynapseSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceAzureSynapseSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceAzureSynapseSourceFiltersNamespace"


class GetSourceSourceAzureSynapseSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceAzureSynapseSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceSourceClickHouseSource(BaseModel):
    typename__: Literal["ClickHouseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceClickHouseSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceClickHouseSourceCredential"
    windows: List["GetSourceSourceClickHouseSourceWindows"]
    segmentations: List["GetSourceSourceClickHouseSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceClickHouseSourceNamespace"
    tags: List["GetSourceSourceClickHouseSourceTags"]
    filters: List["GetSourceSourceClickHouseSourceFilters"]
    config: "GetSourceSourceClickHouseSourceConfig"


class GetSourceSourceClickHouseSourceCatalogAsset(BaseModel):
    typename__: Literal["ClickHouseCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceClickHouseSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceClickHouseSourceCredentialNamespace"


class GetSourceSourceClickHouseSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceClickHouseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceClickHouseSourceWindowsNamespace"


class GetSourceSourceClickHouseSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceClickHouseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceClickHouseSourceSegmentationsNamespace"


class GetSourceSourceClickHouseSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceClickHouseSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceClickHouseSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceClickHouseSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceClickHouseSourceFiltersNamespace"


class GetSourceSourceClickHouseSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceClickHouseSourceConfig(BaseModel):
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceSourceDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceDatabricksSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceDatabricksSourceCredential"
    windows: List["GetSourceSourceDatabricksSourceWindows"]
    segmentations: List["GetSourceSourceDatabricksSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceDatabricksSourceNamespace"
    tags: List["GetSourceSourceDatabricksSourceTags"]
    filters: List["GetSourceSourceDatabricksSourceFilters"]
    config: "GetSourceSourceDatabricksSourceConfig"


class GetSourceSourceDatabricksSourceCatalogAsset(BaseModel):
    typename__: Literal["DatabricksCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceDatabricksSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceDatabricksSourceCredentialNamespace"


class GetSourceSourceDatabricksSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceDatabricksSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceDatabricksSourceWindowsNamespace"


class GetSourceSourceDatabricksSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceDatabricksSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceDatabricksSourceSegmentationsNamespace"


class GetSourceSourceDatabricksSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceDatabricksSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceDatabricksSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceDatabricksSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceDatabricksSourceFiltersNamespace"


class GetSourceSourceDatabricksSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceDatabricksSourceConfig(BaseModel):
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]
    http_path: Optional[str] = Field(alias="httpPath")


class GetSourceSourceDbtModelRunSource(BaseModel):
    typename__: Literal["DbtModelRunSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceDbtModelRunSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceDbtModelRunSourceCredential"
    windows: List["GetSourceSourceDbtModelRunSourceWindows"]
    segmentations: List["GetSourceSourceDbtModelRunSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceDbtModelRunSourceNamespace"
    tags: List["GetSourceSourceDbtModelRunSourceTags"]
    filters: List["GetSourceSourceDbtModelRunSourceFilters"]
    config: "GetSourceSourceDbtModelRunSourceConfig"


class GetSourceSourceDbtModelRunSourceCatalogAsset(BaseModel):
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


class GetSourceSourceDbtModelRunSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceDbtModelRunSourceCredentialNamespace"


class GetSourceSourceDbtModelRunSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceDbtModelRunSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceDbtModelRunSourceWindowsNamespace"


class GetSourceSourceDbtModelRunSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceDbtModelRunSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceDbtModelRunSourceSegmentationsNamespace"


class GetSourceSourceDbtModelRunSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceDbtModelRunSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceDbtModelRunSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceDbtModelRunSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceDbtModelRunSourceFiltersNamespace"


class GetSourceSourceDbtModelRunSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceDbtModelRunSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class GetSourceSourceDbtTestResultSource(BaseModel):
    typename__: Literal["DbtTestResultSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceDbtTestResultSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceDbtTestResultSourceCredential"
    windows: List["GetSourceSourceDbtTestResultSourceWindows"]
    segmentations: List["GetSourceSourceDbtTestResultSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceDbtTestResultSourceNamespace"
    tags: List["GetSourceSourceDbtTestResultSourceTags"]
    filters: List["GetSourceSourceDbtTestResultSourceFilters"]
    config: "GetSourceSourceDbtTestResultSourceConfig"


class GetSourceSourceDbtTestResultSourceCatalogAsset(BaseModel):
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


class GetSourceSourceDbtTestResultSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceDbtTestResultSourceCredentialNamespace"


class GetSourceSourceDbtTestResultSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceDbtTestResultSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceDbtTestResultSourceWindowsNamespace"


class GetSourceSourceDbtTestResultSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceDbtTestResultSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceDbtTestResultSourceSegmentationsNamespace"


class GetSourceSourceDbtTestResultSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceDbtTestResultSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceDbtTestResultSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceDbtTestResultSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceDbtTestResultSourceFiltersNamespace"


class GetSourceSourceDbtTestResultSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceDbtTestResultSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class GetSourceSourceGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceGcpBigQuerySourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceGcpBigQuerySourceCredential"
    windows: List["GetSourceSourceGcpBigQuerySourceWindows"]
    segmentations: List["GetSourceSourceGcpBigQuerySourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceGcpBigQuerySourceNamespace"
    tags: List["GetSourceSourceGcpBigQuerySourceTags"]
    filters: List["GetSourceSourceGcpBigQuerySourceFilters"]
    config: "GetSourceSourceGcpBigQuerySourceConfig"


class GetSourceSourceGcpBigQuerySourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceGcpBigQuerySourceCredential(BaseModel):
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
    namespace: "GetSourceSourceGcpBigQuerySourceCredentialNamespace"


class GetSourceSourceGcpBigQuerySourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpBigQuerySourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceGcpBigQuerySourceWindowsNamespace"


class GetSourceSourceGcpBigQuerySourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpBigQuerySourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceGcpBigQuerySourceSegmentationsNamespace"


class GetSourceSourceGcpBigQuerySourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpBigQuerySourceNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpBigQuerySourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceGcpBigQuerySourceFilters(BaseModel):
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
    namespace: "GetSourceSourceGcpBigQuerySourceFiltersNamespace"


class GetSourceSourceGcpBigQuerySourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpBigQuerySourceConfig(BaseModel):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceSourceGcpPubSubLiteSource(BaseModel):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceGcpPubSubLiteSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceGcpPubSubLiteSourceCredential"
    windows: List["GetSourceSourceGcpPubSubLiteSourceWindows"]
    segmentations: List["GetSourceSourceGcpPubSubLiteSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceGcpPubSubLiteSourceNamespace"
    tags: List["GetSourceSourceGcpPubSubLiteSourceTags"]
    filters: List["GetSourceSourceGcpPubSubLiteSourceFilters"]
    config: "GetSourceSourceGcpPubSubLiteSourceConfig"


class GetSourceSourceGcpPubSubLiteSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubLiteCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceGcpPubSubLiteSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceGcpPubSubLiteSourceCredentialNamespace"


class GetSourceSourceGcpPubSubLiteSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpPubSubLiteSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceGcpPubSubLiteSourceWindowsNamespace"


class GetSourceSourceGcpPubSubLiteSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpPubSubLiteSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceGcpPubSubLiteSourceSegmentationsNamespace"


class GetSourceSourceGcpPubSubLiteSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpPubSubLiteSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpPubSubLiteSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceGcpPubSubLiteSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceGcpPubSubLiteSourceFiltersNamespace"


class GetSourceSourceGcpPubSubLiteSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpPubSubLiteSourceConfig(BaseModel):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "GetSourceSourceGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceSourceGcpPubSubLiteSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceSourceGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceGcpPubSubSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceGcpPubSubSourceCredential"
    windows: List["GetSourceSourceGcpPubSubSourceWindows"]
    segmentations: List["GetSourceSourceGcpPubSubSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceGcpPubSubSourceNamespace"
    tags: List["GetSourceSourceGcpPubSubSourceTags"]
    filters: List["GetSourceSourceGcpPubSubSourceFilters"]
    config: "GetSourceSourceGcpPubSubSourceConfig"


class GetSourceSourceGcpPubSubSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceGcpPubSubSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceGcpPubSubSourceCredentialNamespace"


class GetSourceSourceGcpPubSubSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpPubSubSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceGcpPubSubSourceWindowsNamespace"


class GetSourceSourceGcpPubSubSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpPubSubSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceGcpPubSubSourceSegmentationsNamespace"


class GetSourceSourceGcpPubSubSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpPubSubSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpPubSubSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceGcpPubSubSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceGcpPubSubSourceFiltersNamespace"


class GetSourceSourceGcpPubSubSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpPubSubSourceConfig(BaseModel):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional["GetSourceSourceGcpPubSubSourceConfigMessageFormat"] = (
        Field(alias="messageFormat")
    )


class GetSourceSourceGcpPubSubSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceSourceGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceGcpStorageSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceGcpStorageSourceCredential"
    windows: List["GetSourceSourceGcpStorageSourceWindows"]
    segmentations: List["GetSourceSourceGcpStorageSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceGcpStorageSourceNamespace"
    tags: List["GetSourceSourceGcpStorageSourceTags"]
    filters: List["GetSourceSourceGcpStorageSourceFilters"]
    config: "GetSourceSourceGcpStorageSourceConfig"


class GetSourceSourceGcpStorageSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpStorageCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceGcpStorageSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceGcpStorageSourceCredentialNamespace"


class GetSourceSourceGcpStorageSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpStorageSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceGcpStorageSourceWindowsNamespace"


class GetSourceSourceGcpStorageSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpStorageSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceGcpStorageSourceSegmentationsNamespace"


class GetSourceSourceGcpStorageSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpStorageSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpStorageSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceGcpStorageSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceGcpStorageSourceFiltersNamespace"


class GetSourceSourceGcpStorageSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceGcpStorageSourceConfig(BaseModel):
    project: str
    bucket: str
    folder: str
    csv: Optional["GetSourceSourceGcpStorageSourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceSourceGcpStorageSourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceSourceKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceKafkaSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceKafkaSourceCredential"
    windows: List["GetSourceSourceKafkaSourceWindows"]
    segmentations: List["GetSourceSourceKafkaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceKafkaSourceNamespace"
    tags: List["GetSourceSourceKafkaSourceTags"]
    filters: List["GetSourceSourceKafkaSourceFilters"]
    config: "GetSourceSourceKafkaSourceConfig"


class GetSourceSourceKafkaSourceCatalogAsset(BaseModel):
    typename__: Literal["KafkaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceKafkaSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceKafkaSourceCredentialNamespace"


class GetSourceSourceKafkaSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceKafkaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceKafkaSourceWindowsNamespace"


class GetSourceSourceKafkaSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceKafkaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceKafkaSourceSegmentationsNamespace"


class GetSourceSourceKafkaSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceKafkaSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceKafkaSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceKafkaSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceKafkaSourceFiltersNamespace"


class GetSourceSourceKafkaSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional["GetSourceSourceKafkaSourceConfigMessageFormat"] = Field(
        alias="messageFormat"
    )


class GetSourceSourceKafkaSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceSourcePostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourcePostgreSqlSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourcePostgreSqlSourceCredential"
    windows: List["GetSourceSourcePostgreSqlSourceWindows"]
    segmentations: List["GetSourceSourcePostgreSqlSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourcePostgreSqlSourceNamespace"
    tags: List["GetSourceSourcePostgreSqlSourceTags"]
    filters: List["GetSourceSourcePostgreSqlSourceFilters"]
    config: "GetSourceSourcePostgreSqlSourceConfig"


class GetSourceSourcePostgreSqlSourceCatalogAsset(BaseModel):
    typename__: Literal["PostgreSqlCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourcePostgreSqlSourceCredential(BaseModel):
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
    namespace: "GetSourceSourcePostgreSqlSourceCredentialNamespace"


class GetSourceSourcePostgreSqlSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourcePostgreSqlSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourcePostgreSqlSourceWindowsNamespace"


class GetSourceSourcePostgreSqlSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourcePostgreSqlSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourcePostgreSqlSourceSegmentationsNamespace"


class GetSourceSourcePostgreSqlSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourcePostgreSqlSourceNamespace(BaseModel):
    id: Any


class GetSourceSourcePostgreSqlSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourcePostgreSqlSourceFilters(BaseModel):
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
    namespace: "GetSourceSourcePostgreSqlSourceFiltersNamespace"


class GetSourceSourcePostgreSqlSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourcePostgreSqlSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceSourceSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceSnowflakeSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceSnowflakeSourceCredential"
    windows: List["GetSourceSourceSnowflakeSourceWindows"]
    segmentations: List["GetSourceSourceSnowflakeSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceSnowflakeSourceNamespace"
    tags: List["GetSourceSourceSnowflakeSourceTags"]
    filters: List["GetSourceSourceSnowflakeSourceFilters"]
    config: "GetSourceSourceSnowflakeSourceConfig"


class GetSourceSourceSnowflakeSourceCatalogAsset(BaseModel):
    typename__: Literal["SnowflakeCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceSnowflakeSourceCredential(BaseModel):
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
    namespace: "GetSourceSourceSnowflakeSourceCredentialNamespace"


class GetSourceSourceSnowflakeSourceCredentialNamespace(BaseModel):
    id: Any


class GetSourceSourceSnowflakeSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceSnowflakeSourceWindowsNamespace"


class GetSourceSourceSnowflakeSourceWindowsNamespace(BaseModel):
    id: Any


class GetSourceSourceSnowflakeSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceSourceSnowflakeSourceSegmentationsNamespace"


class GetSourceSourceSnowflakeSourceSegmentationsNamespace(BaseModel):
    id: Any


class GetSourceSourceSnowflakeSourceNamespace(BaseModel):
    id: Any


class GetSourceSourceSnowflakeSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceSourceSnowflakeSourceFilters(BaseModel):
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
    namespace: "GetSourceSourceSnowflakeSourceFiltersNamespace"


class GetSourceSourceSnowflakeSourceFiltersNamespace(BaseModel):
    id: Any


class GetSourceSourceSnowflakeSourceConfig(BaseModel):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


GetSource.model_rebuild()
GetSourceSourceSource.model_rebuild()
GetSourceSourceSourceCredential.model_rebuild()
GetSourceSourceSourceWindows.model_rebuild()
GetSourceSourceSourceSegmentations.model_rebuild()
GetSourceSourceSourceFilters.model_rebuild()
GetSourceSourceAwsAthenaSource.model_rebuild()
GetSourceSourceAwsAthenaSourceCredential.model_rebuild()
GetSourceSourceAwsAthenaSourceWindows.model_rebuild()
GetSourceSourceAwsAthenaSourceSegmentations.model_rebuild()
GetSourceSourceAwsAthenaSourceFilters.model_rebuild()
GetSourceSourceAwsKinesisSource.model_rebuild()
GetSourceSourceAwsKinesisSourceCredential.model_rebuild()
GetSourceSourceAwsKinesisSourceWindows.model_rebuild()
GetSourceSourceAwsKinesisSourceSegmentations.model_rebuild()
GetSourceSourceAwsKinesisSourceFilters.model_rebuild()
GetSourceSourceAwsKinesisSourceConfig.model_rebuild()
GetSourceSourceAwsRedshiftSource.model_rebuild()
GetSourceSourceAwsRedshiftSourceCredential.model_rebuild()
GetSourceSourceAwsRedshiftSourceWindows.model_rebuild()
GetSourceSourceAwsRedshiftSourceSegmentations.model_rebuild()
GetSourceSourceAwsRedshiftSourceFilters.model_rebuild()
GetSourceSourceAwsS3Source.model_rebuild()
GetSourceSourceAwsS3SourceCredential.model_rebuild()
GetSourceSourceAwsS3SourceWindows.model_rebuild()
GetSourceSourceAwsS3SourceSegmentations.model_rebuild()
GetSourceSourceAwsS3SourceFilters.model_rebuild()
GetSourceSourceAwsS3SourceConfig.model_rebuild()
GetSourceSourceAzureSynapseSource.model_rebuild()
GetSourceSourceAzureSynapseSourceCredential.model_rebuild()
GetSourceSourceAzureSynapseSourceWindows.model_rebuild()
GetSourceSourceAzureSynapseSourceSegmentations.model_rebuild()
GetSourceSourceAzureSynapseSourceFilters.model_rebuild()
GetSourceSourceClickHouseSource.model_rebuild()
GetSourceSourceClickHouseSourceCredential.model_rebuild()
GetSourceSourceClickHouseSourceWindows.model_rebuild()
GetSourceSourceClickHouseSourceSegmentations.model_rebuild()
GetSourceSourceClickHouseSourceFilters.model_rebuild()
GetSourceSourceDatabricksSource.model_rebuild()
GetSourceSourceDatabricksSourceCredential.model_rebuild()
GetSourceSourceDatabricksSourceWindows.model_rebuild()
GetSourceSourceDatabricksSourceSegmentations.model_rebuild()
GetSourceSourceDatabricksSourceFilters.model_rebuild()
GetSourceSourceDbtModelRunSource.model_rebuild()
GetSourceSourceDbtModelRunSourceCredential.model_rebuild()
GetSourceSourceDbtModelRunSourceWindows.model_rebuild()
GetSourceSourceDbtModelRunSourceSegmentations.model_rebuild()
GetSourceSourceDbtModelRunSourceFilters.model_rebuild()
GetSourceSourceDbtTestResultSource.model_rebuild()
GetSourceSourceDbtTestResultSourceCredential.model_rebuild()
GetSourceSourceDbtTestResultSourceWindows.model_rebuild()
GetSourceSourceDbtTestResultSourceSegmentations.model_rebuild()
GetSourceSourceDbtTestResultSourceFilters.model_rebuild()
GetSourceSourceGcpBigQuerySource.model_rebuild()
GetSourceSourceGcpBigQuerySourceCredential.model_rebuild()
GetSourceSourceGcpBigQuerySourceWindows.model_rebuild()
GetSourceSourceGcpBigQuerySourceSegmentations.model_rebuild()
GetSourceSourceGcpBigQuerySourceFilters.model_rebuild()
GetSourceSourceGcpPubSubLiteSource.model_rebuild()
GetSourceSourceGcpPubSubLiteSourceCredential.model_rebuild()
GetSourceSourceGcpPubSubLiteSourceWindows.model_rebuild()
GetSourceSourceGcpPubSubLiteSourceSegmentations.model_rebuild()
GetSourceSourceGcpPubSubLiteSourceFilters.model_rebuild()
GetSourceSourceGcpPubSubLiteSourceConfig.model_rebuild()
GetSourceSourceGcpPubSubSource.model_rebuild()
GetSourceSourceGcpPubSubSourceCredential.model_rebuild()
GetSourceSourceGcpPubSubSourceWindows.model_rebuild()
GetSourceSourceGcpPubSubSourceSegmentations.model_rebuild()
GetSourceSourceGcpPubSubSourceFilters.model_rebuild()
GetSourceSourceGcpPubSubSourceConfig.model_rebuild()
GetSourceSourceGcpStorageSource.model_rebuild()
GetSourceSourceGcpStorageSourceCredential.model_rebuild()
GetSourceSourceGcpStorageSourceWindows.model_rebuild()
GetSourceSourceGcpStorageSourceSegmentations.model_rebuild()
GetSourceSourceGcpStorageSourceFilters.model_rebuild()
GetSourceSourceGcpStorageSourceConfig.model_rebuild()
GetSourceSourceKafkaSource.model_rebuild()
GetSourceSourceKafkaSourceCredential.model_rebuild()
GetSourceSourceKafkaSourceWindows.model_rebuild()
GetSourceSourceKafkaSourceSegmentations.model_rebuild()
GetSourceSourceKafkaSourceFilters.model_rebuild()
GetSourceSourceKafkaSourceConfig.model_rebuild()
GetSourceSourcePostgreSqlSource.model_rebuild()
GetSourceSourcePostgreSqlSourceCredential.model_rebuild()
GetSourceSourcePostgreSqlSourceWindows.model_rebuild()
GetSourceSourcePostgreSqlSourceSegmentations.model_rebuild()
GetSourceSourcePostgreSqlSourceFilters.model_rebuild()
GetSourceSourceSnowflakeSource.model_rebuild()
GetSourceSourceSnowflakeSourceCredential.model_rebuild()
GetSourceSourceSnowflakeSourceWindows.model_rebuild()
GetSourceSourceSnowflakeSourceSegmentations.model_rebuild()
GetSourceSourceSnowflakeSourceFilters.model_rebuild()

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


class ListSources(BaseModel):
    sources_list: List[
        Annotated[
            Union[
                "ListSourcesSourcesListSource",
                "ListSourcesSourcesListAwsAthenaSource",
                "ListSourcesSourcesListAwsKinesisSource",
                "ListSourcesSourcesListAwsRedshiftSource",
                "ListSourcesSourcesListAwsS3Source",
                "ListSourcesSourcesListAzureSynapseSource",
                "ListSourcesSourcesListClickHouseSource",
                "ListSourcesSourcesListDatabricksSource",
                "ListSourcesSourcesListDbtModelRunSource",
                "ListSourcesSourcesListDbtTestResultSource",
                "ListSourcesSourcesListGcpBigQuerySource",
                "ListSourcesSourcesListGcpPubSubLiteSource",
                "ListSourcesSourcesListGcpPubSubSource",
                "ListSourcesSourcesListGcpStorageSource",
                "ListSourcesSourcesListKafkaSource",
                "ListSourcesSourcesListPostgreSqlSource",
                "ListSourcesSourcesListSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourcesList")


class ListSourcesSourcesListSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "ListSourcesSourcesListSourceCredential"
    windows: List["ListSourcesSourcesListSourceWindows"]
    segmentations: List["ListSourcesSourcesListSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListSourceNamespace"
    tags: List["ListSourcesSourcesListSourceTags"]
    filters: List["ListSourcesSourcesListSourceFilters"]


class ListSourcesSourcesListSourceCatalogAsset(BaseModel):
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


class ListSourcesSourcesListSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListSourceCredentialNamespace"


class ListSourcesSourcesListSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListSourceWindowsNamespace"


class ListSourcesSourcesListSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListSourceSegmentationsNamespace"


class ListSourcesSourcesListSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListSourceFiltersNamespace"


class ListSourcesSourcesListSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListAwsAthenaSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListAwsAthenaSourceCredential"
    windows: List["ListSourcesSourcesListAwsAthenaSourceWindows"]
    segmentations: List["ListSourcesSourcesListAwsAthenaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAwsAthenaSourceNamespace"
    tags: List["ListSourcesSourcesListAwsAthenaSourceTags"]
    filters: List["ListSourcesSourcesListAwsAthenaSourceFilters"]
    config: "ListSourcesSourcesListAwsAthenaSourceConfig"


class ListSourcesSourcesListAwsAthenaSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsAthenaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListAwsAthenaSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListAwsAthenaSourceCredentialNamespace"


class ListSourcesSourcesListAwsAthenaSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsAthenaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAwsAthenaSourceWindowsNamespace"


class ListSourcesSourcesListAwsAthenaSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsAthenaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAwsAthenaSourceSegmentationsNamespace"


class ListSourcesSourcesListAwsAthenaSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsAthenaSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsAthenaSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListAwsAthenaSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListAwsAthenaSourceFiltersNamespace"


class ListSourcesSourcesListAwsAthenaSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsAthenaSourceConfig(BaseModel):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListAwsKinesisSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListAwsKinesisSourceCredential"
    windows: List["ListSourcesSourcesListAwsKinesisSourceWindows"]
    segmentations: List["ListSourcesSourcesListAwsKinesisSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAwsKinesisSourceNamespace"
    tags: List["ListSourcesSourcesListAwsKinesisSourceTags"]
    filters: List["ListSourcesSourcesListAwsKinesisSourceFilters"]
    config: "ListSourcesSourcesListAwsKinesisSourceConfig"


class ListSourcesSourcesListAwsKinesisSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsKinesisCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListAwsKinesisSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListAwsKinesisSourceCredentialNamespace"


class ListSourcesSourcesListAwsKinesisSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsKinesisSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAwsKinesisSourceWindowsNamespace"


class ListSourcesSourcesListAwsKinesisSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsKinesisSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAwsKinesisSourceSegmentationsNamespace"


class ListSourcesSourcesListAwsKinesisSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsKinesisSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsKinesisSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListAwsKinesisSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListAwsKinesisSourceFiltersNamespace"


class ListSourcesSourcesListAwsKinesisSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsKinesisSourceConfig(BaseModel):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional[
        "ListSourcesSourcesListAwsKinesisSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class ListSourcesSourcesListAwsKinesisSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class ListSourcesSourcesListAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListAwsRedshiftSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListAwsRedshiftSourceCredential"
    windows: List["ListSourcesSourcesListAwsRedshiftSourceWindows"]
    segmentations: List["ListSourcesSourcesListAwsRedshiftSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAwsRedshiftSourceNamespace"
    tags: List["ListSourcesSourcesListAwsRedshiftSourceTags"]
    filters: List["ListSourcesSourcesListAwsRedshiftSourceFilters"]
    config: "ListSourcesSourcesListAwsRedshiftSourceConfig"


class ListSourcesSourcesListAwsRedshiftSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsRedshiftCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListAwsRedshiftSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListAwsRedshiftSourceCredentialNamespace"


class ListSourcesSourcesListAwsRedshiftSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsRedshiftSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAwsRedshiftSourceWindowsNamespace"


class ListSourcesSourcesListAwsRedshiftSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsRedshiftSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAwsRedshiftSourceSegmentationsNamespace"


class ListSourcesSourcesListAwsRedshiftSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsRedshiftSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsRedshiftSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListAwsRedshiftSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListAwsRedshiftSourceFiltersNamespace"


class ListSourcesSourcesListAwsRedshiftSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsRedshiftSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListAwsS3SourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "ListSourcesSourcesListAwsS3SourceCredential"
    windows: List["ListSourcesSourcesListAwsS3SourceWindows"]
    segmentations: List["ListSourcesSourcesListAwsS3SourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAwsS3SourceNamespace"
    tags: List["ListSourcesSourcesListAwsS3SourceTags"]
    filters: List["ListSourcesSourcesListAwsS3SourceFilters"]
    config: "ListSourcesSourcesListAwsS3SourceConfig"


class ListSourcesSourcesListAwsS3SourceCatalogAsset(BaseModel):
    typename__: Literal["AwsS3CatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListAwsS3SourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListAwsS3SourceCredentialNamespace"


class ListSourcesSourcesListAwsS3SourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsS3SourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAwsS3SourceWindowsNamespace"


class ListSourcesSourcesListAwsS3SourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsS3SourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAwsS3SourceSegmentationsNamespace"


class ListSourcesSourcesListAwsS3SourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsS3SourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsS3SourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListAwsS3SourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListAwsS3SourceFiltersNamespace"


class ListSourcesSourcesListAwsS3SourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional["ListSourcesSourcesListAwsS3SourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class ListSourcesSourcesListAwsS3SourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class ListSourcesSourcesListAzureSynapseSource(BaseModel):
    typename__: Literal["AzureSynapseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListAzureSynapseSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListAzureSynapseSourceCredential"
    windows: List["ListSourcesSourcesListAzureSynapseSourceWindows"]
    segmentations: List["ListSourcesSourcesListAzureSynapseSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAzureSynapseSourceNamespace"
    tags: List["ListSourcesSourcesListAzureSynapseSourceTags"]
    filters: List["ListSourcesSourcesListAzureSynapseSourceFilters"]
    config: "ListSourcesSourcesListAzureSynapseSourceConfig"


class ListSourcesSourcesListAzureSynapseSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListAzureSynapseSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListAzureSynapseSourceCredentialNamespace"


class ListSourcesSourcesListAzureSynapseSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAzureSynapseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAzureSynapseSourceWindowsNamespace"


class ListSourcesSourcesListAzureSynapseSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAzureSynapseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListAzureSynapseSourceSegmentationsNamespace"


class ListSourcesSourcesListAzureSynapseSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAzureSynapseSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAzureSynapseSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListAzureSynapseSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListAzureSynapseSourceFiltersNamespace"


class ListSourcesSourcesListAzureSynapseSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListAzureSynapseSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListClickHouseSource(BaseModel):
    typename__: Literal["ClickHouseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListClickHouseSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListClickHouseSourceCredential"
    windows: List["ListSourcesSourcesListClickHouseSourceWindows"]
    segmentations: List["ListSourcesSourcesListClickHouseSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListClickHouseSourceNamespace"
    tags: List["ListSourcesSourcesListClickHouseSourceTags"]
    filters: List["ListSourcesSourcesListClickHouseSourceFilters"]
    config: "ListSourcesSourcesListClickHouseSourceConfig"


class ListSourcesSourcesListClickHouseSourceCatalogAsset(BaseModel):
    typename__: Literal["ClickHouseCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListClickHouseSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListClickHouseSourceCredentialNamespace"


class ListSourcesSourcesListClickHouseSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListClickHouseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListClickHouseSourceWindowsNamespace"


class ListSourcesSourcesListClickHouseSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListClickHouseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListClickHouseSourceSegmentationsNamespace"


class ListSourcesSourcesListClickHouseSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListClickHouseSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListClickHouseSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListClickHouseSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListClickHouseSourceFiltersNamespace"


class ListSourcesSourcesListClickHouseSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListClickHouseSourceConfig(BaseModel):
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListDatabricksSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListDatabricksSourceCredential"
    windows: List["ListSourcesSourcesListDatabricksSourceWindows"]
    segmentations: List["ListSourcesSourcesListDatabricksSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListDatabricksSourceNamespace"
    tags: List["ListSourcesSourcesListDatabricksSourceTags"]
    filters: List["ListSourcesSourcesListDatabricksSourceFilters"]
    config: "ListSourcesSourcesListDatabricksSourceConfig"


class ListSourcesSourcesListDatabricksSourceCatalogAsset(BaseModel):
    typename__: Literal["DatabricksCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListDatabricksSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListDatabricksSourceCredentialNamespace"


class ListSourcesSourcesListDatabricksSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDatabricksSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListDatabricksSourceWindowsNamespace"


class ListSourcesSourcesListDatabricksSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDatabricksSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListDatabricksSourceSegmentationsNamespace"


class ListSourcesSourcesListDatabricksSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDatabricksSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDatabricksSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListDatabricksSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListDatabricksSourceFiltersNamespace"


class ListSourcesSourcesListDatabricksSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDatabricksSourceConfig(BaseModel):
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]
    http_path: Optional[str] = Field(alias="httpPath")


class ListSourcesSourcesListDbtModelRunSource(BaseModel):
    typename__: Literal["DbtModelRunSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListDbtModelRunSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListDbtModelRunSourceCredential"
    windows: List["ListSourcesSourcesListDbtModelRunSourceWindows"]
    segmentations: List["ListSourcesSourcesListDbtModelRunSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListDbtModelRunSourceNamespace"
    tags: List["ListSourcesSourcesListDbtModelRunSourceTags"]
    filters: List["ListSourcesSourcesListDbtModelRunSourceFilters"]
    config: "ListSourcesSourcesListDbtModelRunSourceConfig"


class ListSourcesSourcesListDbtModelRunSourceCatalogAsset(BaseModel):
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


class ListSourcesSourcesListDbtModelRunSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListDbtModelRunSourceCredentialNamespace"


class ListSourcesSourcesListDbtModelRunSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDbtModelRunSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListDbtModelRunSourceWindowsNamespace"


class ListSourcesSourcesListDbtModelRunSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDbtModelRunSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListDbtModelRunSourceSegmentationsNamespace"


class ListSourcesSourcesListDbtModelRunSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDbtModelRunSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDbtModelRunSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListDbtModelRunSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListDbtModelRunSourceFiltersNamespace"


class ListSourcesSourcesListDbtModelRunSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDbtModelRunSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListDbtTestResultSource(BaseModel):
    typename__: Literal["DbtTestResultSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListDbtTestResultSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListDbtTestResultSourceCredential"
    windows: List["ListSourcesSourcesListDbtTestResultSourceWindows"]
    segmentations: List["ListSourcesSourcesListDbtTestResultSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListDbtTestResultSourceNamespace"
    tags: List["ListSourcesSourcesListDbtTestResultSourceTags"]
    filters: List["ListSourcesSourcesListDbtTestResultSourceFilters"]
    config: "ListSourcesSourcesListDbtTestResultSourceConfig"


class ListSourcesSourcesListDbtTestResultSourceCatalogAsset(BaseModel):
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


class ListSourcesSourcesListDbtTestResultSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListDbtTestResultSourceCredentialNamespace"


class ListSourcesSourcesListDbtTestResultSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDbtTestResultSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListDbtTestResultSourceWindowsNamespace"


class ListSourcesSourcesListDbtTestResultSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDbtTestResultSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListDbtTestResultSourceSegmentationsNamespace"


class ListSourcesSourcesListDbtTestResultSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDbtTestResultSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDbtTestResultSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListDbtTestResultSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListDbtTestResultSourceFiltersNamespace"


class ListSourcesSourcesListDbtTestResultSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListDbtTestResultSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListGcpBigQuerySourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListGcpBigQuerySourceCredential"
    windows: List["ListSourcesSourcesListGcpBigQuerySourceWindows"]
    segmentations: List["ListSourcesSourcesListGcpBigQuerySourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListGcpBigQuerySourceNamespace"
    tags: List["ListSourcesSourcesListGcpBigQuerySourceTags"]
    filters: List["ListSourcesSourcesListGcpBigQuerySourceFilters"]
    config: "ListSourcesSourcesListGcpBigQuerySourceConfig"


class ListSourcesSourcesListGcpBigQuerySourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListGcpBigQuerySourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListGcpBigQuerySourceCredentialNamespace"


class ListSourcesSourcesListGcpBigQuerySourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpBigQuerySourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListGcpBigQuerySourceWindowsNamespace"


class ListSourcesSourcesListGcpBigQuerySourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpBigQuerySourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListGcpBigQuerySourceSegmentationsNamespace"


class ListSourcesSourcesListGcpBigQuerySourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpBigQuerySourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpBigQuerySourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListGcpBigQuerySourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListGcpBigQuerySourceFiltersNamespace"


class ListSourcesSourcesListGcpBigQuerySourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpBigQuerySourceConfig(BaseModel):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListGcpPubSubLiteSource(BaseModel):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListGcpPubSubLiteSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListGcpPubSubLiteSourceCredential"
    windows: List["ListSourcesSourcesListGcpPubSubLiteSourceWindows"]
    segmentations: List["ListSourcesSourcesListGcpPubSubLiteSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListGcpPubSubLiteSourceNamespace"
    tags: List["ListSourcesSourcesListGcpPubSubLiteSourceTags"]
    filters: List["ListSourcesSourcesListGcpPubSubLiteSourceFilters"]
    config: "ListSourcesSourcesListGcpPubSubLiteSourceConfig"


class ListSourcesSourcesListGcpPubSubLiteSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubLiteCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListGcpPubSubLiteSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListGcpPubSubLiteSourceCredentialNamespace"


class ListSourcesSourcesListGcpPubSubLiteSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpPubSubLiteSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListGcpPubSubLiteSourceWindowsNamespace"


class ListSourcesSourcesListGcpPubSubLiteSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpPubSubLiteSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListGcpPubSubLiteSourceSegmentationsNamespace"


class ListSourcesSourcesListGcpPubSubLiteSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpPubSubLiteSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpPubSubLiteSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListGcpPubSubLiteSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListGcpPubSubLiteSourceFiltersNamespace"


class ListSourcesSourcesListGcpPubSubLiteSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpPubSubLiteSourceConfig(BaseModel):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "ListSourcesSourcesListGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class ListSourcesSourcesListGcpPubSubLiteSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class ListSourcesSourcesListGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListGcpPubSubSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListGcpPubSubSourceCredential"
    windows: List["ListSourcesSourcesListGcpPubSubSourceWindows"]
    segmentations: List["ListSourcesSourcesListGcpPubSubSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListGcpPubSubSourceNamespace"
    tags: List["ListSourcesSourcesListGcpPubSubSourceTags"]
    filters: List["ListSourcesSourcesListGcpPubSubSourceFilters"]
    config: "ListSourcesSourcesListGcpPubSubSourceConfig"


class ListSourcesSourcesListGcpPubSubSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListGcpPubSubSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListGcpPubSubSourceCredentialNamespace"


class ListSourcesSourcesListGcpPubSubSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpPubSubSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListGcpPubSubSourceWindowsNamespace"


class ListSourcesSourcesListGcpPubSubSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpPubSubSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListGcpPubSubSourceSegmentationsNamespace"


class ListSourcesSourcesListGcpPubSubSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpPubSubSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpPubSubSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListGcpPubSubSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListGcpPubSubSourceFiltersNamespace"


class ListSourcesSourcesListGcpPubSubSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpPubSubSourceConfig(BaseModel):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "ListSourcesSourcesListGcpPubSubSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class ListSourcesSourcesListGcpPubSubSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class ListSourcesSourcesListGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListGcpStorageSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListGcpStorageSourceCredential"
    windows: List["ListSourcesSourcesListGcpStorageSourceWindows"]
    segmentations: List["ListSourcesSourcesListGcpStorageSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListGcpStorageSourceNamespace"
    tags: List["ListSourcesSourcesListGcpStorageSourceTags"]
    filters: List["ListSourcesSourcesListGcpStorageSourceFilters"]
    config: "ListSourcesSourcesListGcpStorageSourceConfig"


class ListSourcesSourcesListGcpStorageSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpStorageCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListGcpStorageSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListGcpStorageSourceCredentialNamespace"


class ListSourcesSourcesListGcpStorageSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpStorageSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListGcpStorageSourceWindowsNamespace"


class ListSourcesSourcesListGcpStorageSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpStorageSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListGcpStorageSourceSegmentationsNamespace"


class ListSourcesSourcesListGcpStorageSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpStorageSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpStorageSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListGcpStorageSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListGcpStorageSourceFiltersNamespace"


class ListSourcesSourcesListGcpStorageSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListGcpStorageSourceConfig(BaseModel):
    project: str
    bucket: str
    folder: str
    csv: Optional["ListSourcesSourcesListGcpStorageSourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class ListSourcesSourcesListGcpStorageSourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class ListSourcesSourcesListKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListKafkaSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "ListSourcesSourcesListKafkaSourceCredential"
    windows: List["ListSourcesSourcesListKafkaSourceWindows"]
    segmentations: List["ListSourcesSourcesListKafkaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListKafkaSourceNamespace"
    tags: List["ListSourcesSourcesListKafkaSourceTags"]
    filters: List["ListSourcesSourcesListKafkaSourceFilters"]
    config: "ListSourcesSourcesListKafkaSourceConfig"


class ListSourcesSourcesListKafkaSourceCatalogAsset(BaseModel):
    typename__: Literal["KafkaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListKafkaSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListKafkaSourceCredentialNamespace"


class ListSourcesSourcesListKafkaSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListKafkaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListKafkaSourceWindowsNamespace"


class ListSourcesSourcesListKafkaSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListKafkaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListKafkaSourceSegmentationsNamespace"


class ListSourcesSourcesListKafkaSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListKafkaSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListKafkaSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListKafkaSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListKafkaSourceFiltersNamespace"


class ListSourcesSourcesListKafkaSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional["ListSourcesSourcesListKafkaSourceConfigMessageFormat"] = (
        Field(alias="messageFormat")
    )


class ListSourcesSourcesListKafkaSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class ListSourcesSourcesListPostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListPostgreSqlSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListPostgreSqlSourceCredential"
    windows: List["ListSourcesSourcesListPostgreSqlSourceWindows"]
    segmentations: List["ListSourcesSourcesListPostgreSqlSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListPostgreSqlSourceNamespace"
    tags: List["ListSourcesSourcesListPostgreSqlSourceTags"]
    filters: List["ListSourcesSourcesListPostgreSqlSourceFilters"]
    config: "ListSourcesSourcesListPostgreSqlSourceConfig"


class ListSourcesSourcesListPostgreSqlSourceCatalogAsset(BaseModel):
    typename__: Literal["PostgreSqlCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListPostgreSqlSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListPostgreSqlSourceCredentialNamespace"


class ListSourcesSourcesListPostgreSqlSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListPostgreSqlSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListPostgreSqlSourceWindowsNamespace"


class ListSourcesSourcesListPostgreSqlSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListPostgreSqlSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListPostgreSqlSourceSegmentationsNamespace"


class ListSourcesSourcesListPostgreSqlSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListPostgreSqlSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListPostgreSqlSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListPostgreSqlSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListPostgreSqlSourceFiltersNamespace"


class ListSourcesSourcesListPostgreSqlSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListPostgreSqlSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListSnowflakeSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListSnowflakeSourceCredential"
    windows: List["ListSourcesSourcesListSnowflakeSourceWindows"]
    segmentations: List["ListSourcesSourcesListSnowflakeSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListSnowflakeSourceNamespace"
    tags: List["ListSourcesSourcesListSnowflakeSourceTags"]
    filters: List["ListSourcesSourcesListSnowflakeSourceFilters"]
    config: "ListSourcesSourcesListSnowflakeSourceConfig"


class ListSourcesSourcesListSnowflakeSourceCatalogAsset(BaseModel):
    typename__: Literal["SnowflakeCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListSnowflakeSourceCredential(BaseModel):
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
    namespace: "ListSourcesSourcesListSnowflakeSourceCredentialNamespace"


class ListSourcesSourcesListSnowflakeSourceCredentialNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListSnowflakeSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListSnowflakeSourceWindowsNamespace"


class ListSourcesSourcesListSnowflakeSourceWindowsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListSnowflakeSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListSourcesSourcesListSnowflakeSourceSegmentationsNamespace"


class ListSourcesSourcesListSnowflakeSourceSegmentationsNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListSnowflakeSourceNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListSnowflakeSourceTags(BaseModel):
    key: str
    value: Optional[str]


class ListSourcesSourcesListSnowflakeSourceFilters(BaseModel):
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
    namespace: "ListSourcesSourcesListSnowflakeSourceFiltersNamespace"


class ListSourcesSourcesListSnowflakeSourceFiltersNamespace(BaseModel):
    id: Any


class ListSourcesSourcesListSnowflakeSourceConfig(BaseModel):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


ListSources.model_rebuild()
ListSourcesSourcesListSource.model_rebuild()
ListSourcesSourcesListSourceCredential.model_rebuild()
ListSourcesSourcesListSourceWindows.model_rebuild()
ListSourcesSourcesListSourceSegmentations.model_rebuild()
ListSourcesSourcesListSourceFilters.model_rebuild()
ListSourcesSourcesListAwsAthenaSource.model_rebuild()
ListSourcesSourcesListAwsAthenaSourceCredential.model_rebuild()
ListSourcesSourcesListAwsAthenaSourceWindows.model_rebuild()
ListSourcesSourcesListAwsAthenaSourceSegmentations.model_rebuild()
ListSourcesSourcesListAwsAthenaSourceFilters.model_rebuild()
ListSourcesSourcesListAwsKinesisSource.model_rebuild()
ListSourcesSourcesListAwsKinesisSourceCredential.model_rebuild()
ListSourcesSourcesListAwsKinesisSourceWindows.model_rebuild()
ListSourcesSourcesListAwsKinesisSourceSegmentations.model_rebuild()
ListSourcesSourcesListAwsKinesisSourceFilters.model_rebuild()
ListSourcesSourcesListAwsKinesisSourceConfig.model_rebuild()
ListSourcesSourcesListAwsRedshiftSource.model_rebuild()
ListSourcesSourcesListAwsRedshiftSourceCredential.model_rebuild()
ListSourcesSourcesListAwsRedshiftSourceWindows.model_rebuild()
ListSourcesSourcesListAwsRedshiftSourceSegmentations.model_rebuild()
ListSourcesSourcesListAwsRedshiftSourceFilters.model_rebuild()
ListSourcesSourcesListAwsS3Source.model_rebuild()
ListSourcesSourcesListAwsS3SourceCredential.model_rebuild()
ListSourcesSourcesListAwsS3SourceWindows.model_rebuild()
ListSourcesSourcesListAwsS3SourceSegmentations.model_rebuild()
ListSourcesSourcesListAwsS3SourceFilters.model_rebuild()
ListSourcesSourcesListAwsS3SourceConfig.model_rebuild()
ListSourcesSourcesListAzureSynapseSource.model_rebuild()
ListSourcesSourcesListAzureSynapseSourceCredential.model_rebuild()
ListSourcesSourcesListAzureSynapseSourceWindows.model_rebuild()
ListSourcesSourcesListAzureSynapseSourceSegmentations.model_rebuild()
ListSourcesSourcesListAzureSynapseSourceFilters.model_rebuild()
ListSourcesSourcesListClickHouseSource.model_rebuild()
ListSourcesSourcesListClickHouseSourceCredential.model_rebuild()
ListSourcesSourcesListClickHouseSourceWindows.model_rebuild()
ListSourcesSourcesListClickHouseSourceSegmentations.model_rebuild()
ListSourcesSourcesListClickHouseSourceFilters.model_rebuild()
ListSourcesSourcesListDatabricksSource.model_rebuild()
ListSourcesSourcesListDatabricksSourceCredential.model_rebuild()
ListSourcesSourcesListDatabricksSourceWindows.model_rebuild()
ListSourcesSourcesListDatabricksSourceSegmentations.model_rebuild()
ListSourcesSourcesListDatabricksSourceFilters.model_rebuild()
ListSourcesSourcesListDbtModelRunSource.model_rebuild()
ListSourcesSourcesListDbtModelRunSourceCredential.model_rebuild()
ListSourcesSourcesListDbtModelRunSourceWindows.model_rebuild()
ListSourcesSourcesListDbtModelRunSourceSegmentations.model_rebuild()
ListSourcesSourcesListDbtModelRunSourceFilters.model_rebuild()
ListSourcesSourcesListDbtTestResultSource.model_rebuild()
ListSourcesSourcesListDbtTestResultSourceCredential.model_rebuild()
ListSourcesSourcesListDbtTestResultSourceWindows.model_rebuild()
ListSourcesSourcesListDbtTestResultSourceSegmentations.model_rebuild()
ListSourcesSourcesListDbtTestResultSourceFilters.model_rebuild()
ListSourcesSourcesListGcpBigQuerySource.model_rebuild()
ListSourcesSourcesListGcpBigQuerySourceCredential.model_rebuild()
ListSourcesSourcesListGcpBigQuerySourceWindows.model_rebuild()
ListSourcesSourcesListGcpBigQuerySourceSegmentations.model_rebuild()
ListSourcesSourcesListGcpBigQuerySourceFilters.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSource.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSourceCredential.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSourceWindows.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSourceSegmentations.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSourceFilters.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSourceConfig.model_rebuild()
ListSourcesSourcesListGcpPubSubSource.model_rebuild()
ListSourcesSourcesListGcpPubSubSourceCredential.model_rebuild()
ListSourcesSourcesListGcpPubSubSourceWindows.model_rebuild()
ListSourcesSourcesListGcpPubSubSourceSegmentations.model_rebuild()
ListSourcesSourcesListGcpPubSubSourceFilters.model_rebuild()
ListSourcesSourcesListGcpPubSubSourceConfig.model_rebuild()
ListSourcesSourcesListGcpStorageSource.model_rebuild()
ListSourcesSourcesListGcpStorageSourceCredential.model_rebuild()
ListSourcesSourcesListGcpStorageSourceWindows.model_rebuild()
ListSourcesSourcesListGcpStorageSourceSegmentations.model_rebuild()
ListSourcesSourcesListGcpStorageSourceFilters.model_rebuild()
ListSourcesSourcesListGcpStorageSourceConfig.model_rebuild()
ListSourcesSourcesListKafkaSource.model_rebuild()
ListSourcesSourcesListKafkaSourceCredential.model_rebuild()
ListSourcesSourcesListKafkaSourceWindows.model_rebuild()
ListSourcesSourcesListKafkaSourceSegmentations.model_rebuild()
ListSourcesSourcesListKafkaSourceFilters.model_rebuild()
ListSourcesSourcesListKafkaSourceConfig.model_rebuild()
ListSourcesSourcesListPostgreSqlSource.model_rebuild()
ListSourcesSourcesListPostgreSqlSourceCredential.model_rebuild()
ListSourcesSourcesListPostgreSqlSourceWindows.model_rebuild()
ListSourcesSourcesListPostgreSqlSourceSegmentations.model_rebuild()
ListSourcesSourcesListPostgreSqlSourceFilters.model_rebuild()
ListSourcesSourcesListSnowflakeSource.model_rebuild()
ListSourcesSourcesListSnowflakeSourceCredential.model_rebuild()
ListSourcesSourcesListSnowflakeSourceWindows.model_rebuild()
ListSourcesSourcesListSnowflakeSourceSegmentations.model_rebuild()
ListSourcesSourcesListSnowflakeSourceFilters.model_rebuild()

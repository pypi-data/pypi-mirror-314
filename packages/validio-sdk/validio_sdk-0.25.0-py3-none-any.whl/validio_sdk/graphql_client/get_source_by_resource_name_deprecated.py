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


class GetSourceByResourceNameDeprecated(BaseModel):
    source_by_resource_name: Optional[
        Annotated[
            Union[
                "GetSourceByResourceNameDeprecatedSourceByResourceNameSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3Source",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceByResourceName")


class GetSourceByResourceNameDeprecatedSourceByResourceNameSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameSourceCredential"
    windows: List["GetSourceByResourceNameDeprecatedSourceByResourceNameSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameSourceNamespace"
    tags: List["GetSourceByResourceNameDeprecatedSourceByResourceNameSourceTags"]
    filters: List["GetSourceByResourceNameDeprecatedSourceByResourceNameSourceFilters"]


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceCatalogAsset(
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


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceCredential(BaseModel):
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
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSourceCredentialNamespace"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSourceWindowsNamespace"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceNamespace(BaseModel):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceFilters(BaseModel):
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
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSourceFiltersNamespace"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceNamespace"
    )
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceFilters"
    ]
    config: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceConfig"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["AwsAthenaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceConfig(
    BaseModel
):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceNamespace"
    )
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceFilters"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["AwsKinesisCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceConfig(
    BaseModel
):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceNamespace"
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceFilters"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["AwsRedshiftCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceConfig(
    BaseModel
):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceNamespace"
    )
    tags: List["GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceTags"]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceFilters"
    ]
    config: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceConfig"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceCatalogAsset(
    BaseModel
):
    typename__: Literal["AwsS3CatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceConfigCsv"
    ]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceConfigCsv(
    BaseModel
):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSource(
    BaseModel
):
    typename__: Literal["AzureSynapseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceNamespace"
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceFilters"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceConfig(
    BaseModel
):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSource(BaseModel):
    typename__: Literal["ClickHouseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceNamespace"
    )
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceFilters"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["ClickHouseCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceConfig(
    BaseModel
):
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceNamespace"
    )
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceFilters"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["DatabricksCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceConfig(
    BaseModel
):
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]
    http_path: Optional[str] = Field(alias="httpPath")


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSource(BaseModel):
    typename__: Literal["DbtModelRunSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceNamespace"
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceFilters"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceCatalogAsset(
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


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceConfig(
    BaseModel
):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSource(
    BaseModel
):
    typename__: Literal["DbtTestResultSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceNamespace"
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceFilters"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceCatalogAsset(
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


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceConfig(
    BaseModel
):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceNamespace"
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceFilters"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceCatalogAsset(
    BaseModel
):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceConfig(
    BaseModel
):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSource(
    BaseModel
):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceNamespace"
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceFilters"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["GcpPubSubLiteCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceConfig(
    BaseModel
):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceNamespace"
    )
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceFilters"
    ]
    config: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceConfig"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["GcpPubSubCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceConfig(
    BaseModel
):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceNamespace"
    )
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceFilters"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["GcpStorageCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceConfig(
    BaseModel
):
    project: str
    bucket: str
    folder: str
    csv: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceConfigCsv"
    ]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceConfigCsv(
    BaseModel
):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceNamespace"
    )
    tags: List["GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceTags"]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceFilters"
    ]
    config: "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceConfig"


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["KafkaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceTags(BaseModel):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceNamespace"
    )
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceFilters"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["PostgreSqlCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceConfig(
    BaseModel
):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceNamespace"
    )
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceTags"
    ]
    filters: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceFilters"
    ]
    config: "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceConfig"


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["SnowflakeCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceCredential(
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceCredentialNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceCredentialNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceWindowsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceWindowsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceSegmentationsNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceFilters(
    BaseModel
):
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
    namespace: "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceFiltersNamespace"


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceFiltersNamespace(
    BaseModel
):
    id: Any


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceConfig(
    BaseModel
):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


GetSourceByResourceNameDeprecated.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceConfig.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3Source.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceConfig.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceConfig.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceConfig.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceConfig.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceConfig.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceFilters.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceCredential.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceWindows.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceSegmentations.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceFilters.model_rebuild()

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
from .fragments import ErrorDetails


class UpdateSourceOwner(BaseModel):
    source_owner_update: "UpdateSourceOwnerSourceOwnerUpdate" = Field(
        alias="sourceOwnerUpdate"
    )


class UpdateSourceOwnerSourceOwnerUpdate(BaseModel):
    errors: List["UpdateSourceOwnerSourceOwnerUpdateErrors"]
    source: Optional[
        Annotated[
            Union[
                "UpdateSourceOwnerSourceOwnerUpdateSourceSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3Source",
                "UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSource",
                "UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class UpdateSourceOwnerSourceOwnerUpdateErrors(ErrorDetails):
    pass


class UpdateSourceOwnerSourceOwnerUpdateSourceSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceSourceWindows"]
    segmentations: List["UpdateSourceOwnerSourceOwnerUpdateSourceSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceSourceFilters"]


class UpdateSourceOwnerSourceOwnerUpdateSourceSourceCatalogAsset(BaseModel):
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


class UpdateSourceOwnerSourceOwnerUpdateSourceSourceCredential(BaseModel):
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
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceSourceCredentialNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceSourceCredentialNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceSourceWindowsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceSourceWindowsNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceSourceSegmentationsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceSourceSegmentationsNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceSourceFilters(BaseModel):
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
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceSourceFiltersNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceSourceFiltersNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsAthenaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceWindowsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceSegmentationsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceFilters(BaseModel):
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
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceFiltersNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceConfig(BaseModel):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsKinesisCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceWindowsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceSegmentationsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceFilters(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceFiltersNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceConfig(BaseModel):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsRedshiftCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceWindowsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceSegmentationsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceFilters(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceFiltersNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceCatalogAsset(BaseModel):
    typename__: Literal["AwsS3CatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceCredential(BaseModel):
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
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceCredentialNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceCredentialNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceWindowsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceWindowsNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceSegmentationsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceFilters(BaseModel):
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
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceFiltersNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceFiltersNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional["UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSource(BaseModel):
    typename__: Literal["AzureSynapseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceWindowsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceSegmentationsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceFilters(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceFiltersNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSource(BaseModel):
    typename__: Literal["ClickHouseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceCatalogAsset(BaseModel):
    typename__: Literal["ClickHouseCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceWindowsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceSegmentationsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceFilters(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceFiltersNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceConfig(BaseModel):
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceCatalogAsset(BaseModel):
    typename__: Literal["DatabricksCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceWindowsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceSegmentationsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceFilters(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceFiltersNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceConfig(BaseModel):
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]
    http_path: Optional[str] = Field(alias="httpPath")


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSource(BaseModel):
    typename__: Literal["DbtModelRunSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceCatalogAsset(BaseModel):
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


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceWindowsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceSegmentationsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceFilters(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceFiltersNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSource(BaseModel):
    typename__: Literal["DbtTestResultSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceCatalogAsset(
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


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceWindowsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceSegmentationsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceFilters(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceFiltersNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceWindowsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceSegmentationsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceFilters(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceFiltersNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceConfig(BaseModel):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSource(BaseModel):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceCatalogAsset(
    BaseModel
):
    typename__: Literal["GcpPubSubLiteCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceWindowsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceSegmentationsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceFilters(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceFiltersNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceConfig(BaseModel):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceWindowsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceSegmentationsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceFilters(BaseModel):
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
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceFiltersNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceConfig(BaseModel):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpStorageCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceWindowsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceSegmentationsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceFilters(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceFiltersNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceConfig(BaseModel):
    project: str
    bucket: str
    folder: str
    csv: Optional["UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceCatalogAsset(BaseModel):
    typename__: Literal["KafkaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceCredential(BaseModel):
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
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceCredentialNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceCredentialNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceWindowsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceWindowsNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceSegmentationsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceFilters(BaseModel):
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
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceFiltersNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceFiltersNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceCatalogAsset(BaseModel):
    typename__: Literal["PostgreSqlCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceWindowsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceSegmentationsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceFilters(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceFiltersNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional[
        "UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    credential: "UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceCredential"
    windows: List["UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceWindows"]
    segmentations: List[
        "UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceNamespace"
    tags: List["UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceTags"]
    filters: List["UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceFilters"]
    config: "UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceConfig"


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceCatalogAsset(BaseModel):
    typename__: Literal["SnowflakeCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceCredential(BaseModel):
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
        "UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceCredentialNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceCredentialNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceWindowsNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceWindowsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceSegmentationsNamespace"
    )


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceSegmentationsNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceNamespace(BaseModel):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceTags(BaseModel):
    key: str
    value: Optional[str]


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceFilters(BaseModel):
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
    namespace: "UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceFiltersNamespace"


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceFiltersNamespace(
    BaseModel
):
    id: Any


class UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceConfig(BaseModel):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


UpdateSourceOwner.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdate.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsAthenaSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsKinesisSourceConfig.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsRedshiftSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3Source.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAwsS3SourceConfig.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceAzureSynapseSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceClickHouseSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDatabricksSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDbtModelRunSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceDbtTestResultSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpBigQuerySourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubLiteSourceConfig.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpPubSubSourceConfig.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceGcpStorageSourceConfig.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceKafkaSourceConfig.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourcePostgreSqlSourceFilters.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSource.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceCredential.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceWindows.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceSegmentations.model_rebuild()
UpdateSourceOwnerSourceOwnerUpdateSourceSnowflakeSourceFilters.model_rebuild()

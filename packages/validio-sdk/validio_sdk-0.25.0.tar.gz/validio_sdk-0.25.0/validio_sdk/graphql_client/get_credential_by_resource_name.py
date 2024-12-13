from datetime import datetime
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import CredentialId

from .base_model import BaseModel
from .enums import AzureSynapseBackendType, ClickHouseProtocol
from .fragments import CredentialBase


class GetCredentialByResourceName(BaseModel):
    credential_by_resource_name: Optional[
        Annotated[
            Union[
                "GetCredentialByResourceNameCredentialByResourceNameCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAzureSynapseEntraIdCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAzureSynapseSqlCredential",
                "GetCredentialByResourceNameCredentialByResourceNameClickHouseCredential",
                "GetCredentialByResourceNameCredentialByResourceNameDatabricksCredential",
                "GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredential",
                "GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredential",
                "GetCredentialByResourceNameCredentialByResourceNameGcpCredential",
                "GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredential",
                "GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredential",
                "GetCredentialByResourceNameCredentialByResourceNameLookerCredential",
                "GetCredentialByResourceNameCredentialByResourceNameMsPowerBiCredential",
                "GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential",
                "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential",
                "GetCredentialByResourceNameCredentialByResourceNameTableauConnectedAppCredential",
                "GetCredentialByResourceNameCredentialByResourceNameTableauPersonalAccessTokenCredential",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="credentialByResourceName")


class GetCredentialByResourceNameCredentialByResourceNameCredential(BaseModel):
    typename__: Literal["Credential", "DemoCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNameCredentialNamespace"


class GetCredentialByResourceNameCredentialByResourceNameCredentialNamespace(BaseModel):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredential(BaseModel):
    typename__: Literal["AwsAthenaCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredentialNamespace"
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredentialConfig(
    BaseModel
):
    access_key: str = Field(alias="accessKey")
    region: str
    query_result_location: str = Field(alias="queryResultLocation")


class GetCredentialByResourceNameCredentialByResourceNameAwsCredential(BaseModel):
    typename__: Literal["AwsCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetCredentialByResourceNameCredentialByResourceNameAwsCredentialNamespace"
    )
    config: "GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameAwsCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")


class GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential(
    BaseModel
):
    typename__: Literal["AwsRedshiftCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialNamespace"
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig(
    BaseModel
):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class GetCredentialByResourceNameCredentialByResourceNameAzureSynapseEntraIdCredential(
    BaseModel
):
    typename__: Literal["AzureSynapseEntraIdCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNameAzureSynapseEntraIdCredentialNamespace"
    config: "GetCredentialByResourceNameCredentialByResourceNameAzureSynapseEntraIdCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameAzureSynapseEntraIdCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameAzureSynapseEntraIdCredentialConfig(
    BaseModel
):
    client_id: str = Field(alias="clientId")
    host: str
    port: int
    database: Optional[str]
    backend_type: AzureSynapseBackendType = Field(alias="backendType")


class GetCredentialByResourceNameCredentialByResourceNameAzureSynapseSqlCredential(
    BaseModel
):
    typename__: Literal["AzureSynapseSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNameAzureSynapseSqlCredentialNamespace"
    config: "GetCredentialByResourceNameCredentialByResourceNameAzureSynapseSqlCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameAzureSynapseSqlCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameAzureSynapseSqlCredentialConfig(
    BaseModel
):
    username: str
    host: str
    port: int
    database: Optional[str]
    backend_type: AzureSynapseBackendType = Field(alias="backendType")


class GetCredentialByResourceNameCredentialByResourceNameClickHouseCredential(
    BaseModel
):
    typename__: Literal["ClickHouseCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNameClickHouseCredentialNamespace"
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameClickHouseCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameClickHouseCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameClickHouseCredentialConfig(
    BaseModel
):
    protocol: ClickHouseProtocol
    host: str
    port: int
    username: str
    default_database: str = Field(alias="defaultDatabase")


class GetCredentialByResourceNameCredentialByResourceNameDatabricksCredential(
    BaseModel
):
    typename__: Literal["DatabricksCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNameDatabricksCredentialNamespace"
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameDatabricksCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameDatabricksCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameDatabricksCredentialConfig(
    BaseModel
):
    host: str
    port: int
    http_path: str = Field(alias="httpPath")


class GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredential(BaseModel):
    typename__: Literal["DbtCloudCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredentialNamespace"
    )
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredentialConfig"
    )


class GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredentialConfig(
    BaseModel
):
    warehouse_credential: (
        "GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredentialConfigWarehouseCredential"
    ) = Field(alias="warehouseCredential")
    account_id: str = Field(alias="accountId")
    api_base_url: Optional[str] = Field(alias="apiBaseUrl")


class GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredentialConfigWarehouseCredential(
    CredentialBase
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


class GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredential(BaseModel):
    typename__: Literal["DbtCoreCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredentialNamespace"
    )
    config: "GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredentialConfig(
    BaseModel
):
    warehouse_credential: (
        "GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredentialConfigWarehouseCredential"
    ) = Field(alias="warehouseCredential")


class GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredentialConfigWarehouseCredential(
    CredentialBase
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


class GetCredentialByResourceNameCredentialByResourceNameGcpCredential(BaseModel):
    typename__: Literal["GcpCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetCredentialByResourceNameCredentialByResourceNameGcpCredentialNamespace"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameGcpCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredential(
    BaseModel
):
    typename__: Literal["KafkaSaslSslPlainCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredentialNamespace"
    config: "GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredentialConfig(
    BaseModel
):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    username: str


class GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredential(BaseModel):
    typename__: Literal["KafkaSslCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredentialNamespace"
    )
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredentialConfig(
    BaseModel
):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: str = Field(alias="caCertificate")


class GetCredentialByResourceNameCredentialByResourceNameLookerCredential(BaseModel):
    typename__: Literal["LookerCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetCredentialByResourceNameCredentialByResourceNameLookerCredentialNamespace"
    )
    config: "GetCredentialByResourceNameCredentialByResourceNameLookerCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameLookerCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameLookerCredentialConfig(
    BaseModel
):
    base_url: str = Field(alias="baseUrl")
    client_id: str = Field(alias="clientId")


class GetCredentialByResourceNameCredentialByResourceNameMsPowerBiCredential(BaseModel):
    typename__: Literal["MsPowerBiCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNameMsPowerBiCredentialNamespace"
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameMsPowerBiCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameMsPowerBiCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameMsPowerBiCredentialConfig(
    BaseModel
):
    auth: Union[
        "GetCredentialByResourceNameCredentialByResourceNameMsPowerBiCredentialConfigPowerBiAuthMsPowerBiCredentialAuthEntraId",
    ] = Field(alias="powerBiAuth", discriminator="typename__")


class GetCredentialByResourceNameCredentialByResourceNameMsPowerBiCredentialConfigPowerBiAuthMsPowerBiCredentialAuthEntraId(
    BaseModel
):
    typename__: Literal["MsPowerBiCredentialAuthEntraId"] = Field(alias="__typename")
    client_id: str = Field(alias="clientId")
    tenant_id: str = Field(alias="tenantId")


class GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential(
    BaseModel
):
    typename__: Literal["PostgreSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialNamespace"
    config: (
        "GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig(
    BaseModel
):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential(BaseModel):
    typename__: Literal["SnowflakeCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialNamespace"
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig(
    BaseModel
):
    account: str
    user: str
    role: Optional[str]
    warehouse: Optional[str]
    auth: Optional[
        Annotated[
            Union[
                "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfigAuthSnowflakeCredentialKeyPair",
                "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfigAuthSnowflakeCredentialUserPassword",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfigAuthSnowflakeCredentialKeyPair(
    BaseModel
):
    typename__: Literal["SnowflakeCredentialKeyPair"] = Field(alias="__typename")
    user: str


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfigAuthSnowflakeCredentialUserPassword(
    BaseModel
):
    typename__: Literal["SnowflakeCredentialUserPassword"] = Field(alias="__typename")
    user: str


class GetCredentialByResourceNameCredentialByResourceNameTableauConnectedAppCredential(
    BaseModel
):
    typename__: Literal["TableauConnectedAppCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNameTableauConnectedAppCredentialNamespace"
    config: "GetCredentialByResourceNameCredentialByResourceNameTableauConnectedAppCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameTableauConnectedAppCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameTableauConnectedAppCredentialConfig(
    BaseModel
):
    host: str
    site: Optional[str]
    user: str
    client_id: str = Field(alias="clientId")
    secret_id: str = Field(alias="secretId")


class GetCredentialByResourceNameCredentialByResourceNameTableauPersonalAccessTokenCredential(
    BaseModel
):
    typename__: Literal["TableauPersonalAccessTokenCredential"] = Field(
        alias="__typename"
    )
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetCredentialByResourceNameCredentialByResourceNameTableauPersonalAccessTokenCredentialNamespace"
    config: "GetCredentialByResourceNameCredentialByResourceNameTableauPersonalAccessTokenCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameTableauPersonalAccessTokenCredentialNamespace(
    BaseModel
):
    id: Any


class GetCredentialByResourceNameCredentialByResourceNameTableauPersonalAccessTokenCredentialConfig(
    BaseModel
):
    host: str
    site: Optional[str]
    token_name: str = Field(alias="tokenName")


GetCredentialByResourceName.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAwsCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAzureSynapseEntraIdCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAzureSynapseSqlCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameClickHouseCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameDatabricksCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameGcpCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameLookerCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameMsPowerBiCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameMsPowerBiCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameTableauConnectedAppCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameTableauPersonalAccessTokenCredential.model_rebuild()

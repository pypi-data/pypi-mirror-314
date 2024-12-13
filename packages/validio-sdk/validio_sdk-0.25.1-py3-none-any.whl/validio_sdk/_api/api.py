from datetime import datetime
from enum import Enum
from typing import Any

from aiohttp.client_exceptions import ClientConnectorError
from gql import gql
from gql.transport.exceptions import TransportQueryError
from graphql import DocumentNode, FieldNode, utilities

from validio_sdk.client import Client, Session
from validio_sdk.config import (
    VALIDIO_ACCESS_KEY_ENV,
    VALIDIO_ENDPOINT_ENV,
    VALIDIO_SECRET_ACCESS_KEY_ENV,
    ValidioConfig,
)
from validio_sdk.exception import (
    ForbiddenError,
    UnauthorizedError,
    ValidioConnectionError,
    ValidioError,
)

NUM_CONCURRENT_CONNECTIONS = 5


class APIClient:
    def __init__(self, config: ValidioConfig | None = None):
        self.client = Client(config)

        # We use a somewhat higher timeout that the default 10 seconds to
        # account for longer running operations.
        self.client.client.execute_timeout = 60

    async def execute(self, query: str, **kwargs: Any) -> Any:
        async with self.client as session:
            return await execute(session, query, **kwargs)

    async def execute_mutation(
        self,
        method_name: str,
        argument_types: dict[str, str],
        variable_values: dict[str, Any] | None,
        resource_class_name: str = "",
        returns: str | None = None,
        returns_errors: bool = True,
    ) -> Any:
        async with self.client as session:
            return await execute_mutation(
                session,
                method_name,
                argument_types,
                variable_values,
                resource_class_name,
                returns,
                returns_errors,
            )

    async def infer_schema(
        self,
        class_name: str,
        variable_values: dict[str, Any],
        no_args: bool = False,
    ) -> Any:
        async with self.client as session:
            return await infer_schema(session, class_name, variable_values, no_args)

    async def test_connection(self) -> str | None:
        async with self.client as session:
            return await test_connection(session)

    async def validator_segment_metrics(
        self,
        validator_id: str,
        segment_id: str,
        start_time: datetime,
        end_time: datetime,
    ) -> Any:
        async with self.client as session:
            return await validator_segment_metrics(
                session, validator_id, segment_id, start_time, end_time
            )

    async def get_incidents(
        self,
        validator_id: str,
        start_time: datetime,
        end_time: datetime,
        segment_id: str | None = None,
    ) -> dict[str, Any]:
        async with self.client as session:
            return await get_incidents(
                session, validator_id, start_time, end_time, segment_id
            )

    async def get_credentials(
        self,
        credential_id: str | None = None,
        namespace_id: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        async with self.client as session:
            return await get_credentials(session, credential_id, namespace_id)

    async def get_channels(
        self,
        channel_id: str | None = None,
        namespace_id: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        async with self.client as session:
            return await get_channels(session, channel_id, namespace_id)

    async def get_sources(
        self,
        source_id: str | None = None,
        namespace_id: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        async with self.client as session:
            return await get_sources(session, source_id, namespace_id)

    async def start_source(self, source_id: str) -> Any:
        async with self.client as session:
            return await execute_mutation(
                session,
                "sourceStart",
                argument_types={"id": "SourceId!"},
                variable_values={"id": source_id},
                returns="state",
            )

    async def stop_source(self, source_id: str) -> Any:
        async with self.client as session:
            return await execute_mutation(
                session,
                "sourceStop",
                argument_types={"id": "SourceId!"},
                variable_values={"id": source_id},
                returns="state",
            )

    async def backfill_source(self, source_id: str) -> Any:
        async with self.client as session:
            return await execute_mutation(
                session,
                "sourceBackfill",
                argument_types={"id": "SourceId!"},
                variable_values={"id": source_id},
                returns="state",
            )

    async def reset_source(self, source_id: str) -> Any:
        async with self.client as session:
            return await execute_mutation(
                session,
                "sourceReset",
                argument_types={"id": "SourceId!"},
                variable_values={"id": source_id},
                returns="state",
            )

    async def get_segmentations(
        self,
        segmentation_id: str | None = None,
        namespace_id: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        async with self.client as session:
            return await get_segmentations(session, segmentation_id, namespace_id)

    async def get_segments(
        self,
        segmentation_id: str,
        namespace_id: str | None = None,
    ) -> list[dict[str, Any]]:
        async with self.client as session:
            return await get_segments(session, segmentation_id, namespace_id)

    async def get_windows(
        self,
        window_id: str | None = None,
        namespace_id: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        async with self.client as session:
            return await get_windows(session, window_id, namespace_id)

    async def get_filters(
        self,
        filter_id: str | None = None,
        namespace_id: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        async with self.client as session:
            return await get_filters(session, filter_id, namespace_id)

    async def get_validators(
        self,
        validator_id: str | None = None,
        source_id: str | None = None,
        namespace_id: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        async with self.client as session:
            return await get_validators(session, validator_id, source_id, namespace_id)

    async def get_notification_rules(
        self,
        notification_rule_id: str | None = None,
        namespace_id: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        async with self.client as session:
            return await get_notification_rules(
                session, notification_rule_id, namespace_id
            )

    async def get_namespaces(
        self, namespace_id: str | None = None
    ) -> list[dict[str, Any]] | dict[str, Any]:
        async with self.client as session:
            return await get_namespaces(session, namespace_id)

    async def create_namespace(
        self,
        namespace_id: str,
        name: str,
        members: list[dict[str, str]],
        api_keys: list[dict[str, str]],
    ) -> Any:
        async with self.client as session:
            return await create_namespace(
                session, namespace_id, name, members, api_keys
            )

    async def update_namespace_roles(
        self,
        namespace_id: str,
        members: list[dict[str, str]],
        api_keys: list[dict[str, str]],
    ) -> Any:
        async with self.client as session:
            return await update_namespace_roles(
                session, namespace_id, members, api_keys
            )

    async def delete_namespace(self, namespace_id: str) -> Any:
        async with self.client as session:
            return await delete_namespace(session, namespace_id)

    async def get_recommendations(self, source_id: str) -> Any:
        async with self.client as session:
            return await get_recommendations(session, source_id)

    async def apply_recommendations(self, recommendation_ids: list[str]) -> Any:
        async with self.client as session:
            return await apply_recommendations(session, recommendation_ids)

    async def get_users(
        self,
        user_id: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        async with self.client as session:
            return await get_users(session, user_id)

    async def get_tags(
        self,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        async with self.client as session:
            return await get_tags(session)

    @staticmethod
    def _parse_result(result: Any, q: DocumentNode) -> Any:
        method_name = None

        # Try to find the name of the method called to support shorter result.
        # Get the operation AST and if we only have one selection set and it's a
        # FieldNode, its name is the query or mutation.
        operation_ast = utilities.get_operation_ast(q)
        if operation_ast:
            selection_set = operation_ast.selection_set.selections
            if len(selection_set) == 1 and isinstance(selection_set[0], FieldNode):
                method_name = selection_set[0].name.value

        if method_name is not None and method_name in result:
            return result[method_name]

        return result


def _namespace_filter(namespace_id: str | None) -> dict[str, Any]:
    if namespace_id is None:
        return {}

    return {
        "filter": {
            "namespaceId": namespace_id,
        }
    }


# Due to GraphQL limitations we often have to alias fields if they occur on
# multiple types. This method takes a list of tuples with aliased name and
# actual name and replaces all alias keys with the actual keys in the passed
# dictionary.
def _replace_aliases(d: dict[str, Any], replacements: list[tuple[str, str]]) -> None:
    for alias, actual in replacements:
        if alias not in d:
            continue

        d[actual] = d[alias]
        del d[alias]


async def get_sources(
    session: Session,
    source_id: str | None = None,
    namespace_id: str | None = None,
) -> list[dict[str, Any]] | dict[str, Any]:
    source_details = """
        fragment SourceDetails on Source {
          __typename
          id
          name
          description
          createdAt
          updatedAt
          jtdSchema
          state
          stateUpdatedAt
          resourceName
          namespace {
            id
          }
          credential {
            id
            resourceName
          }
          tags {
            id
            key
            value
          }
          ... on GcpStorageSource {
            config {
              project
              bucket
              folder
              csv {
                nullMarker
                delimiter
              }
              schedule
              filePattern
              fileFormat
            }
          }
          ... on GcpBigQuerySource {
            config {
              project
              dataset
              table
              cursorField
              lookbackDays
              schedule
            }
          }
          ... on GcpPubSubSource {
            config {
              project
              subscriptionId
              messageFormat {
                format
                schema
              }
            }
          }
          ... on GcpPubSubLiteSource {
            config {
              location
              project
              subscriptionId
              messageFormat {
                format
                schema
              }
            }
          }
          ... on AwsAthenaSource {
            config {
              catalog
              database
              table
              cursorField
              lookbackDays
              schedule
            }
          }
          ... on AwsKinesisSource {
            config {
              region
              streamName
              messageFormat {
                format
                schema
              }
            }
          }
          ... on AwsRedshiftSource {
            config {
              database
              schema
              table
              cursorField
              lookbackDays
              schedule
            }
          }
          ... on AwsS3Source {
            config {
              bucket
              prefix
              csv {
                nullMarker
                delimiter
              }
              schedule
              filePattern
              fileFormat
            }
          }
          ... on AzureSynapseSource {
            config {
              database
              schema
              table
              cursorField
              lookbackDays
              schedule
            }
          }
          ... on DatabricksSource {
            config {
              catalog
              schema
              table
              cursorField
              lookbackDays
              schedule
              httpPath
            }
          }
          ... on DbtTestResultSource {
            config {
              jobName
              projectName
              schedule
            }
          }
          ... on DbtModelRunSource {
            config {
              jobName
              projectName
              schedule
            }
          }
          ... on PostgreSqlSource {
            config {
              database
              schema
              table
              cursorField
              lookbackDays
              schedule
            }
          }
          ... on SnowflakeSource {
            config {
              role
              warehouse
              database
              schema
              table
              cursorField
              lookbackDays
              schedule
            }
          }
          ... on KafkaSource {
            config {
              topic
              messageFormat {
                format
                schema
              }
            }
          }
          ... on ClickHouseSource {
            config {
              database
              table
              cursorField
              lookbackDays
              schedule
            }
          }
        }
        """

    if source_id and source_id.startswith("SRC_"):
        query = f"""
            {source_details}

            query Source($id: SourceId!) {{
              source(id: $id) {{
                ...SourceDetails
              }}
            }}
            """
        variable_values = {"id": source_id}
    elif source_id:
        if namespace_id is None:
            raise ValidioError(
                "namespace_id is required when querying by resource name"
            )

        query = f"""
            {source_details}

            query SourceByResourceName(
                  $namespaceId: NamespaceId!,
                  $resourceName: String!
            ) {{
              sourceByResourceName(
                namespaceId: $namespaceId,
                resourceName: $resourceName
              ) {{
                ...SourceDetails
              }}
            }}
            """
        variable_values = {
            "resourceName": source_id,
            "namespaceId": namespace_id,
        }
    else:
        query = f"""
            {source_details}

            query ListSources($filter: ResourceFilter) {{
              sourcesList(filter: $filter) {{
                ...SourceDetails
              }}
            }}
            """
        variable_values = _namespace_filter(namespace_id)

    return await execute(session, query, variable_values=variable_values)


async def secrets_changed_by_field(
    session: Session,
    class_name: str,
    return_fields: set[str],
    variable_values: dict[str, Any],
) -> Any:
    """Check if secrets changed. This is only compatible with APIs that return
    which fields have changed.

    Create a query and input types for the passed class name.
    :param class_name: Name of resource class, e.g. RedshiftCredential
    :param return_fields: Names of the secret fields which will be used to retrieve
    the results of change per field
    :param variable_values: Dictionary with secret fields
    :returns: GraphQL response containing which fields have changed
    """
    lc_first = class_name[0].lower() + class_name[1:]
    method_name = f"{lc_first}SecretChanged"
    input_type = f"{class_name}SecretChangedInput!"

    return_fields_query: str = "\n".join(return_fields)

    query = f"""
    query Op($input: {input_type}) {{
        {method_name}(input: $input) {{
        {return_fields_query}
        errors {{ code message }}
        }}
    }}
    """

    return await execute(session, query, variable_values=variable_values)


async def infer_schema(
    session: Session,
    class_name: str,
    variable_values: dict[str, Any],
    no_args: bool = False,
) -> Any:
    lc_first = class_name[0].lower() + class_name[1:]
    method_name = f"{lc_first}InferSchema"
    input_type = f"{class_name}InferSchemaInput!"

    if no_args:
        query = f"""
        query Op {{
            {method_name}
        }}
        """
        input_variable_values = None
    else:
        query = f"""
        query Op($input: {input_type}) {{
            {method_name}(input: $input)
        }}
        """
        input_variable_values = {"input": variable_values}

    return await execute(session, query, variable_values=input_variable_values)


async def dbt_artifact_multipart_upload_create(
    session: Session, credential_id: str, job_name: str
) -> str:
    response = await execute_mutation(
        session,
        "dbtArtifactMultipartUploadCreate",
        argument_types={"input": "DbtArtifactMultipartUploadCreateInput!"},
        variable_values={
            "input": {
                "credentialId": credential_id,
                "jobName": job_name,
            }
        },
        returns="id",
    )

    if response["errors"]:
        raise ValidioError(
            f'Failed to create dbt multipart upload: {response["errors"]}',
        )

    return response["id"]


async def dbt_artifact_multipart_upload_append_part(
    session: Session, upload_id: str, part: str
) -> None:
    response = await execute_mutation(
        session,
        "dbtArtifactMultipartUploadAppendPart",
        argument_types={"input": "DbtArtifactMultipartUploadAppendPartInput!"},
        variable_values={
            "input": {
                "id": upload_id,
                "part": part,
            }
        },
    )

    if response["errors"]:
        raise ValidioError(
            f'Failed to append dbt multipart upload: {response["errors"]}',
        )


async def dbt_artifact_multipart_upload_complete(
    session: Session, upload_id: str
) -> None:
    response = await execute_mutation(
        session,
        "dbtArtifactMultipartUploadComplete",
        argument_types={"input": "DbtArtifactMultipartUploadCompleteInput!"},
        variable_values={"input": {"id": upload_id}},
    )

    if response["errors"]:
        raise ValidioError(
            f'Failed to finalize dbt multipart upload: {response["errors"]}',
        )


async def test_connection(session: Session) -> str | None:
    query = """
    query ListUsers {
        usersList {
        id
        }
    }
    """

    try:
        await execute(session, query)
    except ValidioConnectionError:
        return "Failed to connect to server"
    except UnauthorizedError:
        return "Unauthorized"
    except ForbiddenError:
        return "Forbidden"

    return None


async def validator_segment_metrics(
    session: Session,
    validator_id: str,
    segment_id: str,
    start_time: datetime,
    end_time: datetime,
) -> Any:
    query = """
    fragment ValidatorMetricDetails on ValidatorMetric {
        __typename
        startTime
        endTime
        isIncident
        value
        severity
        deviation
        ... on ValidatorMetricWithFixedThreshold {
        operator
        bound
        }
        ... on ValidatorMetricWithDynamicThreshold {
        lowerBound
        upperBound
        decisionBoundsType
        isBurnIn
        }
        ... on ValidatorMetricWithDifferenceThreshold {
        maybeLowerBound: lowerBound
        maybeUpperBound: upperBound
        }
    }

    query GetValidatorSegmentMetrics($input: ValidatorSegmentMetricsInput!) {
        validatorSegmentMetrics(input: $input) {
        __typename
        ... on ValidatorMetricWithFixedThresholdHistory {
            values {
            ...ValidatorMetricDetails
            }
        }
        ... on ValidatorMetricWithDynamicThresholdHistory {
            values {
            ...ValidatorMetricDetails
            }
        }
        ... on ValidatorMetricWithDifferenceThresholdHistory {
            values {
            ...ValidatorMetricDetails
            }
        }
        }
    }
    """

    result = await execute(
        session,
        query,
        variable_values={
            "input": {
                "validatorId": validator_id,
                "segmentId": segment_id,
                "timeRange": {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                },
            }
        },
    )

    for i, metric in enumerate(result.get("values", [])):
        _replace_aliases(
            metric,
            [
                ("maybeLowerBound", "lowerBound"),
                ("maybeUpperBound", "upperBound"),
            ],
        )
        result["values"][i] = metric

    return result


async def get_incidents(
    session: Session,
    validator_id: str,
    start_time: datetime,
    end_time: datetime,
    segment_id: str | None = None,
) -> dict[str, Any]:
    query = """
    query GetValidatorIncidents(
        $id: ValidatorId!,
        $range: TimeRangeInput!,
        $segmentId: SegmentId
    ) {
        validator(id: $id) {
        __typename
        id
        metricValueFormat
        incidents(range: $range, segmentId: $segmentId) {
            id
            group {
            id
            }
            value
            deviation
            lowerBound
            upperBound
            status
            severity
            startTime
            endTime
            backfillMode
            createdAt
            updatedAt
        }
        }
    }
    """

    return await execute(
        session,
        query,
        variable_values={
            "id": validator_id,
            "segmentId": segment_id,
            "range": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
            },
        },
    )


async def get_credentials(
    session: Session,
    credential_id: str | None = None,
    namespace_id: str | None = None,
) -> list[dict[str, Any]] | dict[str, Any]:
    credential_details = """
    fragment CredentialBase on Credential {
        __typename
        id
        name
        createdAt
        updatedAt
        resourceName
        namespace {
        id
        }
    }

    fragment CredentialDetails on Credential {
        ... CredentialBase
        ... on AwsCredential {
        config {
            accessKey
        }
        enableCatalog
        }
        ... on AwsAthenaCredential {
        config {
            accessKey
            region
            queryResultLocation
        }
        enableCatalog
        }
        ... on AwsRedshiftCredential {
        config {
            host
            port
            user
            defaultDatabase
        }
        enableCatalog
        }
        ... on AzureSynapseEntraIdCredential {
        config {
            clientId
            host
            port
            database
            backendType
        }
        enableCatalog
        }
        ... on AzureSynapseSqlCredential {
        config {
            username
            host
            port
            database
            backendType
        }
        enableCatalog
        }
        ... on DatabricksCredential {
        config {
            host
            port
            httpPath
        }
        enableCatalog
        }
        ... on ClickHouseCredential {
        config {
            protocol
            host
            port
            username
            defaultDatabase
        }
        enableCatalog
        }
        ... on DbtCloudCredential {
        config {
            warehouseCredential {
            ...CredentialBase
            }
            accountId
            apiBaseUrl
        }
        }
        ... on DbtCoreCredential {
        config {
            warehouseCredential {
            ...CredentialBase
            }
        }
        }
        ... on LookerCredential {
        config {
            baseUrl
            clientId
        }
        enableCatalog
        }
        ... on PostgreSqlCredential {
        config {
            host
            port
            user
            defaultDatabase
        }
        enableCatalog
        }
        ... on SnowflakeCredential {
        config {
            account
            role
            warehouse
            auth {
            __typename
            ... on SnowflakeCredentialKeyPair {
                user
            }
            ... on SnowflakeCredentialUserPassword {
                user
            }
            }
        }
        enableCatalog
        }
        ... on KafkaSslCredential {
        config {
            bootstrapServers
            caCertificate
        }
        enableCatalog
        }
        ... on KafkaSaslSslPlainCredential {
        config {
            bootstrapServers
            username
        }
        enableCatalog
        }
        ... on TableauConnectedAppCredential {
        config {
            host
            site
            user
            clientId
            secretId
        }
        enableCatalog
        }
        ... on TableauPersonalAccessTokenCredential {
        config {
            host
            site
            tokenName
        }
        enableCatalog
        }
        ... on GcpCredential {
        enableCatalog
        }
        ... on MsPowerBiCredential {
        config {
            powerBiAuth: auth {
            __typename
            ... on MsPowerBiCredentialAuthEntraId {
                clientId
                tenantId
            }
            }
        }
        enableCatalog
        }
    }
    """

    if credential_id and not credential_id.startswith("CRD_"):
        query = f"""
        {credential_details}

        query GetCredential($namespaceId: NamespaceId!, $resourceName: String!) {{
            credentialByResourceName(
                namespaceId: $namespaceId,
                resourceName: $resourceName
            ) {{
            ...CredentialDetails
            }}
        }}
        """
        variable_values = {
            "namespaceId": namespace_id,
            "resourceName": credential_id,
        }
    else:
        query = f"""
        {credential_details}
        query ListCredentials($filter: ResourceFilter) {{
            credentialsList(filter: $filter) {{
            ...CredentialDetails
            }}
        }}
        """
        variable_values = _namespace_filter(namespace_id)

    result = await execute(session, query, variable_values=variable_values)

    if isinstance(result, list):
        return_first = False
    else:
        return_first = True
        result = [result]

    for i, credential in enumerate(result):
        _replace_aliases(credential.get("config", {}), [("powerBiAuth", "auth")])
        result[i] = credential

    return result[0] if return_first else result


async def get_channels(
    session: Session,
    channel_id: str | None = None,
    namespace_id: str | None = None,
) -> list[dict[str, Any]] | dict[str, Any]:
    channel_details = """
    fragment ChannelDetails on Channel {
        __typename
        id
        name
        createdAt
        updatedAt
        resourceName
        namespace {
        id
        }
        ... on SlackChannel {
        config {
            slackWebhookUrl: webhookUrl
            timezone
            applicationLinkUrl
            slackChannelId
            interactiveMessageEnabled
        }
        }
        ... on WebhookChannel {
        config {
            webhookUrl
            applicationLinkUrl
            authHeader
        }
        }
        ... on MsTeamsChannel {
        config {
            msTeamsWebhookUrl: webhookUrl
            timezone
            applicationLinkUrl
            msTeamsChannelId
            msTeamsInteractiveMessageEnabled: interactiveMessageEnabled
        }
        }
    }
    """

    if channel_id and not channel_id.startswith("CNL_"):
        query = f"""
        {channel_details}

        query GetChannel($namespaceId: NamespaceId!, $resourceName: String!) {{
            channelByResourceName(
                namespaceId: $namespaceId,
                resourceName: $resourceName
            ) {{
            ...ChannelDetails
            }}
        }}
        """
        variable_values = {
            "namespaceId": namespace_id,
            "resourceName": channel_id,
        }
    else:
        query = f"""
        {channel_details}

        query ListChannels($filter: ResourceFilter) {{
            channelsList(filter: $filter) {{
            ...ChannelDetails
            }}
        }}
        """
        variable_values = _namespace_filter(namespace_id)

    result = await execute(session, query, variable_values=variable_values)

    if isinstance(result, list):
        return_first = False
    else:
        return_first = True
        result = [result]

    for ftr in result:
        _replace_aliases(
            ftr["config"],
            [
                ("slackWebhookUrl", "webhookUrl"),
                ("msTeamsWebhookUrl", "webhookUrl"),
                ("msTeamsInteractiveMessageEnabled", "interactiveMessageEnabled"),
            ],
        )

    return result[0] if return_first else result


async def start_source(session: Session, source_id: str) -> Any:
    return await execute_mutation(
        session,
        "sourceStart",
        argument_types={"id": "SourceId!"},
        variable_values={"id": source_id},
        returns="state",
    )


async def stop_source(session: Session, source_id: str) -> Any:
    return await execute_mutation(
        session,
        "sourceStop",
        argument_types={"id": "SourceId!"},
        variable_values={"id": source_id},
        returns="state",
    )


async def backfill_source(session: Session, source_id: str) -> Any:
    return await execute_mutation(
        session,
        "sourceBackfill",
        argument_types={"id": "SourceId!"},
        variable_values={"id": source_id},
        returns="state",
    )


async def reset_source(session: Session, source_id: str) -> Any:
    return await execute_mutation(
        session,
        "sourceReset",
        argument_types={"id": "SourceId!"},
        variable_values={"id": source_id},
        returns="state",
    )


async def get_segmentations(
    session: Session,
    segmentation_id: str | None = None,
    namespace_id: str | None = None,
) -> list[dict[str, Any]] | dict[str, Any]:
    segmentation_details = """
    fragment SegmentationDetails on Segmentation {
        __typename
        id
        name
        fields
        createdAt
        updatedAt
        resourceName
        namespace {
        id
        }
        source {
        id
        resourceName
        }
        filter {
        id
        resourceName
        }
    }
    """

    if segmentation_id and segmentation_id.startswith("SGM_"):
        query = f"""
        {segmentation_details}

        query Segmentation($id: SegmentationId!) {{
            segmentation(id: $id) {{
            ...SegmentationDetails
            }}
        }}
        """
        variable_values = {"id": segmentation_id}
    elif segmentation_id:
        if namespace_id is None:
            raise ValidioError(
                "namespace_id is required when querying by resource name"
            )

        query = f"""
        {segmentation_details}

        query SegmentationByResourceName(
                $namespaceId: NamespaceId!,
                $resourceName: String!
        ) {{
            segmentationByResourceName(
            namespaceId: $namespaceId,
            resourceName: $resourceName
            ) {{
            ...SegmentationDetails
            }}
        }}
        """
        variable_values = {
            "namespaceId": namespace_id,
            "resourceName": segmentation_id,
        }
    else:
        query = f"""
        {segmentation_details}

        query ListSegmentations($filter: ResourceFilter) {{
            segmentationsList(filter: $filter) {{
            ...SegmentationDetails
            }}
        }}
        """
        variable_values = _namespace_filter(namespace_id)

    return await execute(session, query, variable_values=variable_values)


async def get_segments(
    session: Session,
    segmentation_id: str,
    namespace_id: str | None = None,
) -> list[dict[str, Any]]:
    segment_details = """
    fragment SegmentDetails on Segment {
        id
        muted
        fields {
        field
        value
        }
    }
    """

    if segmentation_id.startswith("SGM_"):
        query = f"""
        {segment_details}

        query Segments($id: SegmentationId!) {{
            segments(id: $id) {{
            ...SegmentDetails
            }}
        }}
        """
        variable_values = {"id": segmentation_id}
    else:
        if namespace_id is None:
            raise ValidioError(
                "namespace_id is required when querying by resource name"
            )

        query = f"""
        {segment_details}

        query SegmentsByResourceName(
            $namespaceId: NamespaceId!,
            $resourceName: String!
        ) {{
            segmentsByResourceName(
            namespaceId: $namespaceId,
            resourceName: $resourceName
            ) {{
            ...SegmentDetails
            }}
        }}
        """
        variable_values = {
            "namespaceId": namespace_id,
            "resourceName": segmentation_id,
        }

    return await execute(session, query, variable_values=variable_values)


async def get_windows(
    session: Session,
    window_id: str | None = None,
    namespace_id: str | None = None,
) -> list[dict[str, Any]] | dict[str, Any]:
    window_details = """
    fragment WindowDetails on Window {
        __typename
        id
        name
        createdAt
        updatedAt
        resourceName
        namespace {
        id
        }
        source {
        resourceName
        }
        ... on FileWindow {
        dataTimeField
        }
        ... on FixedBatchWindow {
        config {
            batchSize
            segmentedBatching
            batchTimeoutSecs
        }
        dataTimeField
        }
        ... on TumblingWindow {
        config {
            windowSize
            timeUnit
            windowTimeoutDisabled
        }
        dataTimeField
        }
    }
    """

    if window_id and window_id.startswith("WDW_"):
        query = f"""
        {window_details}

        query Window($id: WindowId!) {{
            window(id: $id) {{
            ...WindowDetails
            }}
        }}
        """
        variable_values = {"id": window_id}
    elif window_id:
        if namespace_id is None:
            raise ValidioError(
                "namespace_id is required when querying by resource name"
            )

        query = f"""
        {window_details}

        query WindowByResourceName(
                $namespaceId: NamespaceId!,
                $resourceName: String!
        ) {{
            windowByResourceName(
            namespaceId: $namespaceId,
            resourceName: $resourceName
            ) {{
            ...WindowDetails
            }}
        }}
        """
        variable_values = {
            "namespaceId": namespace_id,
            "resourceName": window_id,
        }
    else:
        query = f"""
        {window_details}

        query ListWindows($filter: ResourceFilter) {{
            windowsList(filter: $filter) {{
            ...WindowDetails
            }}
        }}
        """
        variable_values = _namespace_filter(namespace_id)

    return await execute(session, query, variable_values=variable_values)


async def get_filters(
    session: Session,
    filter_id: str | None = None,
    namespace_id: str | None = None,
) -> list[dict[str, Any]] | dict[str, Any]:
    filter_details = """
    fragment FilterDetails on Filter {
        __typename
        id
        name
        createdAt
        updatedAt
        resourceName
        namespace {
        id
        }
        source {
        resourceName
        }
        ... on BooleanFilter {
        config {
            booleanFilterField: field
            booleanFilterOperator: operator
        }
        }
        ... on EnumFilter {
        config {
            enumFilterField: field
            enumFilterOperator: operator
            values
        }
        }
        ... on NullFilter {
        config {
            nullFilterField: field
            nullFilterOperator: operator
        }
        }
        ... on SqlFilter {
        config {
            query
        }
        }
        ... on StringFilter {
        config {
            stringFilterField: field
            stringFilterOperator: operator
            stringFilterValue: value
        }
        }
        ... on ThresholdFilter {
        config {
            thresholdFilterField: field
            thresholdFilterOperator: operator
            thresholdFilterValue: value
        }
        }
    }
    """

    if filter_id and filter_id.startswith("FTR_"):
        query = f"""
        {filter_details}

        query Filter($id: FilterId!) {{
            filter(id: $id) {{
            ...FilterDetails
            }}
        }}
        """
        variable_values = {"id": filter_id}
    elif filter_id:
        if namespace_id is None:
            raise ValidioError(
                "namespace_id is required when querying by resource name"
            )

        query = f"""
        {filter_details}

        query FilterByResourceName(
                $namespaceId: NamespaceId!,
                $resourceName: String!
        ) {{
            filterByResourceName(
            namespaceId: $namespaceId,
            resourceName: $resourceName
            ) {{
            ...FilterDetails
            }}
        }}
        """
        variable_values = {
            "namespaceId": namespace_id,
            "resourceName": filter_id,
        }
    else:
        query = f"""
        {filter_details}

        query ListFilters($filter: ResourceFilter) {{
            filtersList(filter: $filter) {{
            ...FilterDetails
            }}
        }}
        """
        variable_values = _namespace_filter(namespace_id)

    result = await execute(session, query, variable_values=variable_values)

    if not result:
        return result

    if isinstance(result, list):
        return_first = False
    else:
        return_first = True
        result = [result]

    for ftr in result:
        _replace_aliases(
            ftr["config"],
            [
                ("booleanFilterField", "field"),
                ("booleanFilterOperator", "operator"),
                ("enumFilterField", "field"),
                ("enumFilterOperator", "operator"),
                ("nullFilterField", "field"),
                ("nullFilterOperator", "operator"),
                ("stringFilterField", "field"),
                ("stringFilterOperator", "operator"),
                ("stringFilterValue", "value"),
                ("thresholdFilterField", "field"),
                ("thresholdFilterOperator", "operator"),
                ("thresholdFilterValue", "value"),
            ],
        )

    return result[0] if return_first else result


async def get_validators(
    session: Session,
    validator_id: str | None = None,
    source_id: str | None = None,
    namespace_id: str | None = None,
) -> list[dict[str, Any]] | dict[str, Any]:
    if validator_id and source_id:
        raise ValidioError("`source_id` is not supported when passing `validator_id`")

    reference_source_config = """
    referenceSourceConfig {
        source {
        ...ReferenceSourceConfigDetails
        }
        window {
        ...WindowDetails
        }
        history
        offset
        sourceFilter {
        id
        resourceName
        }
    }
    """
    validator_details = f"""
    fragment ThresholdDetails on Threshold {{
        __typename
        ... on FixedThreshold {{
        operator
        value
        }}
        ... on DynamicThreshold {{
        sensitivity
        decisionBoundsType
        }}
        ... on DifferenceThreshold {{
        differenceOperator: operator
        differenceType
        numberOfWindows
        value
        }}
    }}

    fragment ReferenceSourceConfigDetails on Source {{
        __typename
        id
        name
        resourceName
        namespaceId
        namespace {{
        id
        }}
    }}

    fragment WindowDetails on Window {{
        __typename
        id
        name
        resourceName
        namespaceId
        namespace {{
        id
        }}
    }}

    fragment ValidatorDetails on Validator {{
        __typename
        id
        name
        description
        createdAt
        updatedAt
        resourceName
        namespace {{
        id
        }}
        sourceConfig {{
        filter
        segmentation {{
            id
            resourceName
        }}
        source {{
            id
            resourceName
        }}
        window {{
            id
            resourceName
        }}
        sourceFilter {{
            id
            resourceName
        }}
        }}
        tags {{
        id
        key
        value
        }}
        ... on NumericValidator {{
        config {{
            sourceField
            metric
            initializeWithBackfill
            threshold {{
            ...ThresholdDetails
            }}
        }}
        }}
        ... on CategoricalDistributionValidator {{
        config {{
            sourceField
            referenceSourceField
            categoricalDistributionMetric: metric
            initializeWithBackfill
            threshold {{
            ...ThresholdDetails
            }}
        }}
        {reference_source_config}
        }}
        ... on NumericDistributionValidator {{
        config {{
            sourceField
            referenceSourceField
            distributionMetric: metric
            initializeWithBackfill
            threshold {{
            ...ThresholdDetails
            }}
        }}
        {reference_source_config}
        }}
        ... on VolumeValidator {{
        config {{
            optionalSourceField: sourceField
            sourceFields
            volumeMetric: metric
            initializeWithBackfill
            threshold {{
            ...ThresholdDetails
            }}
        }}
        }}
        ... on NumericAnomalyValidator {{
        config {{
            sourceField
            numericAnomalyMetric: metric
            initializeWithBackfill
            threshold {{
            ...ThresholdDetails
            }}
            referenceSourceField
            sensitivity
            minimumReferenceDatapoints
            minimumAbsoluteDifference
            minimumRelativeDifferencePercent
        }}
        {reference_source_config}
        }}
        ... on RelativeTimeValidator {{
        config {{
            sourceFieldMinuend
            sourceFieldSubtrahend
            relativeTimeMetric: metric
            initializeWithBackfill
            threshold {{
            ...ThresholdDetails
            }}
        }}
        }}
        ... on FreshnessValidator {{
        config {{
            initializeWithBackfill
            optionalSourceField: sourceField
            threshold {{
            ...ThresholdDetails
            }}
        }}
        }}
        ... on RelativeVolumeValidator {{
        config {{
            optionalSourceField: sourceField
            optionalReferenceSourceField: referenceSourceField
            relativeVolumeMetric: metric
            initializeWithBackfill
            threshold {{
            ...ThresholdDetails
            }}
        }}
        {reference_source_config}
        }}
        ... on SqlValidator {{
        config {{
            query
            threshold {{
            ...ThresholdDetails
            }}
            initializeWithBackfill
        }}
        }}
    }}
    """

    if validator_id and validator_id.startswith("MTR_"):
        query = f"""
        {validator_details}
        query Validator($id: ValidatorId!) {{
            validator(id: $id) {{
            ...ValidatorDetails
            }}
        }}
        """
        variable_values = {"id": validator_id}
    elif validator_id:
        if namespace_id is None:
            raise ValidioError(
                "namespace_id is required when querying by resource name"
            )

        query = f"""
        {validator_details}

        query ValidatorByResourceName(
            $namespaceId: NamespaceId!,
            $resourceName: String!
        ) {{
            validatorByResourceName(
            namespaceId: $namespaceId,
            resourceName: $resourceName
            ) {{
            ...ValidatorDetails
            }}
        }}
        """
        variable_values = {
            "namespaceId": namespace_id,
            "resourceName": validator_id,
        }
    else:
        query = f"""
        {validator_details}
        query ListValidators($id: SourceId, $filter: ResourceFilter) {{
            validatorsList(id: $id, filter: $filter) {{
            ...ValidatorDetails
            }}
        }}
        """
        variable_values = {
            **_namespace_filter(namespace_id),
        }
        if source_id is not None:
            variable_values["id"] = source_id

    result = await execute(
        session,
        query,
        variable_values=variable_values,
    )

    if not result:
        return result

    if isinstance(result, list):
        return_first = False
    else:
        return_first = True
        result = [result]

    for i, validator in enumerate(result):
        _replace_aliases(
            validator["config"]["threshold"], [("differenceOperator", "operator")]
        )
        _replace_aliases(
            validator["config"],
            [
                ("optionalReferenceSourceField", "referenceSourceField"),
                ("optionalSourceField", "sourceField"),
                ("categoricalDistributionMetric", "metric"),
                ("distributionMetric", "metric"),
                ("numericAnomalyMetric", "metric"),
                ("relativeTimeMetric", "metric"),
                ("relativeVolumeMetric", "metric"),
                ("volumeMetric", "metric"),
            ],
        )

        result[i] = validator

    return result[0] if return_first else result


async def get_notification_rules(
    session: Session,
    notification_rule_id: str | None = None,
    namespace_id: str | None = None,
) -> list[dict[str, Any]] | dict[str, Any]:
    nr_details = """
    fragment NotificationRuleConditions on NotificationRuleCondition {
        __typename
        id
        notificationRuleId
        createdAt
        updatedAt
        ... on SourceNotificationRuleCondition {
        config {
            sources {
            __typename
            id
            name
            resourceName
            }
        }
        }
        ... on SeverityNotificationRuleCondition {
        config {
            severities
        }
        }
        ... on TypeNotificationRuleCondition {
        config {
            types
        }
        }
        ... on OwnerNotificationRuleCondition {
        config {
            owners {
            id
            displayName
            }
        }
        }
        ... on TagNotificationRuleCondition {
        config {
            tags {
            id
            key
            value
            }
        }
        }
        ... on SegmentNotificationRuleCondition {
        config {
            segments {
            field
            value
            }
        }
        }
    }

    fragment NotificationRuleDetails on NotificationRule {
        __typename
        id
        name
        createdAt
        updatedAt
        channel {
        __typename
        resourceName
        }
        conditions {
        ...NotificationRuleConditions
        }
        resourceName
        namespace {
        id
        }
    }
    """

    if notification_rule_id and not notification_rule_id.startswith("NRL_"):
        query = f"""
        {nr_details}

        query NotificationRuleByResourceName(
            $namespaceId: NamespaceId!,
            $resourceName: String!
        ) {{
            notificationRuleByResourceName(
            namespaceId: $namespaceId,
            resourceName: $resourceName
            ) {{
            ...NotificationRuleDetails
            }}
        }}
        """
        variable_values = {
            "namespaceId": namespace_id,
            "resourceName": notification_rule_id,
        }
    else:
        query = f"""
        {nr_details}

        query ListNotificationRules($filter: ResourceFilter) {{
            notificationRulesList(filter: $filter) {{
            ...NotificationRuleDetails
            }}
        }}
        """
        variable_values = _namespace_filter(namespace_id)

    return await execute(session, query, variable_values=variable_values)


async def get_namespaces(
    session: Session, namespace_id: str | None = None
) -> list[dict[str, Any]] | dict[str, Any]:
    namespace_details = """
    fragment ApiKeyDetails on ApiKey {
        id
        name
        createdAt
        updatedAt
        lastUsedAt
        globalRole
    }

    fragment NamespaceDetails on Namespace {
        id
        name
        description
        members {
        role
        user {
            ...UserSummary
        }
        }
        teams {
        role
        team {
            ...TeamDetails
        }
        }
        apiKeys {
        role
        apiKey {
            ...ApiKeyDetails
        }
        }
        users {
        role
        user {
            ...UserSummary
        }
        }
    }

    fragment TeamDetails on Team {
        id
        name
        description
        members {
        id
        displayName
        status
        email
        lastLoginAt
        }
        createdAt
        updatedAt
    }

    fragment UserSummary on User {
        id
        displayName
        fullName
        email
        status
        globalRole
        loginType
        lastLoginAt
        updatedAt
        identities {
        __typename
        ... on LocalIdentity {
            username
        }
        }
    }
    """

    if namespace_id:
        query = f"""
        {namespace_details}

        query Namespace($id: NamespaceId!) {{
            namespace(id: $id) {{
            ...NamespaceDetails
            }}
        }}
        """
        variable_values = {"id": namespace_id}
    else:
        query = f"""
        {namespace_details}

        query Namespaces {{
            namespaces {{
            ...NamespaceDetails
            }}
        }}
        """
        variable_values = {}

    return await execute(session, query, variable_values=variable_values)


async def create_namespace(
    session: Session,
    namespace_id: str,
    name: str,
    members: list[dict[str, str]],
    api_keys: list[dict[str, str]],
) -> Any:
    return await execute_mutation(
        session,
        "namespaceCreate",
        argument_types={"input": "NamespaceCreateInput!"},
        variable_values={
            "input": {
                "id": namespace_id,
                "name": name,
                "apiKeys": api_keys,
                "members": members,
            }
        },
        resource_class_name="namespace",
        returns="id name",
    )


async def update_namespace_roles(
    session: Session,
    namespace_id: str,
    members: list[dict[str, str]],
    api_keys: list[dict[str, str]],
) -> Any:
    return await execute_mutation(
        session,
        "namespaceRolesUpdate",
        argument_types={"input": "NamespaceRolesUpdateInput!"},
        variable_values={
            "input": {
                "namespaceId": namespace_id,
                "apiKeys": api_keys,
                "members": members,
            }
        },
        resource_class_name="namespace",
        returns="""
        id
        name
        apiKeys {
            role
            apiKey {
            id
            name
            }
        }
        users {
            role
            user {
            id
            displayName
            }
        }
        """,
    )


async def delete_namespace(session: Session, namespace_id: str) -> Any:
    return await execute_mutation(
        session,
        "namespacesDelete",
        argument_types={"ids": "[String!]!"},
        variable_values={"ids": [namespace_id]},
    )


async def get_recommendations(session: Session, source_id: str) -> Any:
    query = """
    query GetSourceRecommendedValidators($id: SourceId!) {
        source(id: $id) {
        __typename
        state
        recommendedValidators {
            __typename
            id
            name
            createdAt
            sourceConfig {
            segmentation {
                name
            }
            }
        }
        }
    }
    """

    response = await execute(session, query, variable_values={"id": source_id})

    return response["recommendedValidators"]


async def apply_recommendations(session: Session, recommendation_ids: list[str]) -> Any:
    return await execute_mutation(
        session,
        "validatorRecommendationApply",
        argument_types={"input": "ValidatorRecommendationApplyInput!"},
        variable_values={"input": {"ids": recommendation_ids}},
        returns="successIds failedIds",
        returns_errors=False,
    )


async def get_users(
    session: Session,
    user_id: str | None = None,
) -> list[dict[str, Any]] | dict[str, Any]:
    user_details = """
    fragment IdentityDetails on Identity {
        ... on LocalIdentity {
        __typename
        id
        userId
        username
        createdAt
        }
        ... on FederatedIdentity {
        __typename
        id
        userId
        idp {
            __typename
            id
            name
        }
        createdAt
        }
    }

    fragment NamespaceDetails on Namespace {
        id
        name
    }

    fragment TeamDetails on Team {
        id
        name
        description
        members {
        id
        displayName
        status
        email
        lastLoginAt
        }
        createdAt
        updatedAt
    }

    fragment UserDetails on User {
        ...UserSummary
        identities {
        ...IdentityDetails
        }
        teams {
        ...TeamDetails
        }
        namespaces {
        ...NamespaceDetails
        }
        createdAt
        updatedAt
        lastLoginAt
        resourceName
    }

    fragment UserSummary on User {
        id
        displayName
        fullName
        email
        status
        globalRole
        loginType
        lastLoginAt
        updatedAt
        identities {
        __typename
        ... on LocalIdentity {
            username
        }
        }
    }
    """

    if user_id:
        query = f"""
        {user_details}

        query UserByResourceName($resourceName: String!) {{
            userByResourceName(resourceName: $resourceName) {{
            ...UserDetails
            }}
        }}
        """
        variable_values = {"resourceName": user_id}
    else:
        query = f"""
        {user_details}

        query UsersList {{
            usersList {{
            ...UserDetails
            }}
        }}
        """
        variable_values = {}

    return await execute(session, query, variable_values=variable_values)


async def get_tags(
    session: Session,
) -> list[dict[str, Any]] | dict[str, Any]:
    tag_details = """
    fragment TagDetails on Tag {
        id
        key
        value
        origin
    }
    """

    query = f"""
    {tag_details}
    query ListTags {{
        tagsList {{
        ...TagDetails
        }}
    }}
    """

    return await execute(session, query, variable_values={})


async def execute(session: Session, query: str, **kwargs: Any) -> Any:
    """
    Execute any operation.

    Converts the query to a GraphQL `DocumentNode` and passes it with all
    arguments to the underlying client.

    :param query: A GraphQL query
    :param kwargs: Any argument acceptable for the GraphQL client
    :returns: The inner value of the response or the root response if can't
        be determined.
    """
    graphql_query = gql(query)

    try:
        result = APIClient._parse_result(
            await session.execute(query, **kwargs),
            graphql_query,
        )
    except ClientConnectorError as e:
        raise ValidioConnectionError(VALIDIO_ENDPOINT_ENV, e)
    except TransportQueryError as e:
        if not e.errors:
            raise e

        error_details = e.errors[0]
        extension_code = error_details.get("extensions", {}).get("code")

        match extension_code:
            case "INVALID_API_KEY":
                raise UnauthorizedError(
                    VALIDIO_ACCESS_KEY_ENV, VALIDIO_SECRET_ACCESS_KEY_ENV
                )
            case "FORBIDDEN":
                raise ForbiddenError
            case _:
                raise e

    return result


async def execute_mutation(
    session: Session,
    method_name: str,
    argument_types: dict[str, str],
    variable_values: dict[str, Any] | None,
    resource_class_name: str = "",
    returns: str | None = None,
    returns_errors: bool = True,
) -> Any:
    """
    Execute a mutation.

    This will call `method_name` on a mutation and set up variables to bind
    with. This will work for any create, update or delete operations used
    via IaC.

    An example request would look like this:

        mutation Op(input: DemoCredentialCreateInput!) {
          createDemoCredential(input: $input) {
            id
          }
        }

    :param method_name: The method to call.
    :param argument_types: Key-value map of what type each argument is of.
        The keys must map 1:1 to variable values.
    :param variable_values: The values to send for each type, must match the
        keys in the API definition.

    :returns: The GraphQL response, most often a dictionary.
    """
    input_types = ",".join([f"${k}: {v}" for k, v in argument_types.items()])
    input_vals = ",".join([f"{k}: ${k}" for k in argument_types])

    if returns is None:
        returns = ""

    return_fields = (
        f"""
        {resource_class_name} {{
          {returns}
        }}
        """
        if resource_class_name
        else returns
    )

    returned_error = "errors { code message }" if returns_errors else ""

    query = f"""
    mutation Op({input_types}) {{
      {method_name}({input_vals}) {{
        {return_fields}
        {returned_error}
      }}
    }}
    """

    return await execute(session, query, variable_values=variable_values)


class SourceAction(Enum):
    START = "Start"
    STOP = "Stop"
    BACKFILL = "Backfill"
    RESET = "Reset"


async def apply_source_action(
    session: Session, action: SourceAction, source_id: str
) -> dict[str, Any]:
    query = f"""
        mutation S($id: SourceId!) {{
            source{action.value}(id: $id) {{
                errors {{code message }}
            }}
        }}
    """
    try:
        result = await session.execute(query, variable_values={"id": source_id})
    except TransportQueryError as e:
        if e.errors:
            result = {f"source{action.value}": {"errors": e.errors}}
        else:
            result = {f"source{action.value}": {"errors": [{"message": str(e)}]}}
    return result[f"source{action.value}"]


def split_to_chunks(data: list[Any]) -> list[list[Any]]:
    return split_to_n_chunks(data, NUM_CONCURRENT_CONNECTIONS)


def split_to_n_chunks(data: list[Any], num_of_chunks: int) -> list[list[Any]]:
    return [data[i::num_of_chunks] for i in range(min(num_of_chunks, len(data)))]

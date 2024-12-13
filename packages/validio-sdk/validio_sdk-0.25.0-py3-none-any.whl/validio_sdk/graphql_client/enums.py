from enum import Enum


class ApiErrorCode(str, Enum):
    UNKNOWN = "UNKNOWN"


class AzureSynapseBackendType(str, Enum):
    DEDICATED_SQL_POOL = "DEDICATED_SQL_POOL"
    SERVERLESS_SQL_POOL = "SERVERLESS_SQL_POOL"


class BooleanOperator(str, Enum):
    IS_FALSE = "IS_FALSE"
    IS_TRUE = "IS_TRUE"


class CatalogAssetDescriptionOrigin(str, Enum):
    CATALOG_REFRESH = "CATALOG_REFRESH"
    DBT = "DBT"
    VALIDIO = "VALIDIO"


class CatalogAssetType(str, Enum):
    BUCKET = "BUCKET"
    DASHBOARD = "DASHBOARD"
    EXPLORE = "EXPLORE"
    STREAM = "STREAM"
    TABLE = "TABLE"
    TILE = "TILE"
    WORKBOOK = "WORKBOOK"


class CategoricalDistributionMetric(str, Enum):
    ADDED = "ADDED"
    CHANGED = "CHANGED"
    RELATIVE_ENTROPY = "RELATIVE_ENTROPY"
    REMOVED = "REMOVED"


class ClickHouseProtocol(str, Enum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    NATIVE = "NATIVE"


class ComparisonOperator(str, Enum):
    EQUAL = "EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"


class DecisionBoundsType(str, Enum):
    LOWER = "LOWER"
    UPPER = "UPPER"
    UPPER_AND_LOWER = "UPPER_AND_LOWER"


class DifferenceOperator(str, Enum):
    DECREASING = "DECREASING"
    INCREASING = "INCREASING"
    STRICTLY_DECREASING = "STRICTLY_DECREASING"
    STRICTLY_INCREASING = "STRICTLY_INCREASING"


class DifferenceType(str, Enum):
    ABSOLUTE = "ABSOLUTE"
    PERCENTAGE = "PERCENTAGE"


class EnumOperator(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class FileFormat(str, Enum):
    CSV = "CSV"
    JSON = "JSON"
    PARQUET = "PARQUET"


class IdentityDeleteErrorCode(str, Enum):
    UNKNOWN = "UNKNOWN"


class IdentityProviderCreateErrorCode(str, Enum):
    UNKNOWN = "UNKNOWN"


class IdentityProviderDeleteErrorCode(str, Enum):
    UNKNOWN = "UNKNOWN"


class IdentityProviderUpdateErrorCode(str, Enum):
    UNKNOWN = "UNKNOWN"


class IncidentGroupPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    LOW = "LOW"
    MEDIUM = "MEDIUM"


class IncidentRelationship(str, Enum):
    FIELD_LINEAGE_DOWNSTREAM = "FIELD_LINEAGE_DOWNSTREAM"
    FIELD_LINEAGE_UPSTREAM = "FIELD_LINEAGE_UPSTREAM"
    FRESHNESS_DOWNSTREAM = "FRESHNESS_DOWNSTREAM"
    FRESHNESS_UPSTREAM = "FRESHNESS_UPSTREAM"
    FRESHNESS_WITHIN_SOURCE = "FRESHNESS_WITHIN_SOURCE"
    RELATED_VALIDATOR_WITHIN_SOURCE = "RELATED_VALIDATOR_WITHIN_SOURCE"
    ROW_COUNT_WITHIN_SOURCE = "ROW_COUNT_WITHIN_SOURCE"
    VALIDATOR_FIELD_LINEAGE_UPSTREAM = "VALIDATOR_FIELD_LINEAGE_UPSTREAM"
    VALIDATOR_UPSTREAM_SOURCES = "VALIDATOR_UPSTREAM_SOURCES"
    VOLUME_DOWNSTREAM = "VOLUME_DOWNSTREAM"
    VOLUME_UPSTREAM = "VOLUME_UPSTREAM"


class IncidentSeverity(str, Enum):
    HIGH = "HIGH"
    LOW = "LOW"
    MEDIUM = "MEDIUM"


class IncidentStatus(str, Enum):
    INVESTIGATING = "INVESTIGATING"
    NOT_AN_ANOMALY = "NOT_AN_ANOMALY"
    RESOLVED = "RESOLVED"
    TRIAGE = "TRIAGE"


class IssueTypename(str, Enum):
    GenericSourceError = "GenericSourceError"
    SchemaChangeSourceError = "SchemaChangeSourceError"
    SegmentLimitExceededSourceError = "SegmentLimitExceededSourceError"
    ValidatorIncident = "ValidatorIncident"


class LoginType(str, Enum):
    GUEST = "GUEST"
    REGULAR = "REGULAR"


class MetricValueFormat(str, Enum):
    NUMBER = "NUMBER"
    PERCENTAGE = "PERCENTAGE"
    TIME_INTERVAL = "TIME_INTERVAL"


class NullOperator(str, Enum):
    IS = "IS"
    IS_NOT = "IS_NOT"


class NumericAnomalyMetric(str, Enum):
    COUNT = "COUNT"
    PERCENTAGE = "PERCENTAGE"


class NumericDistributionMetric(str, Enum):
    MAXIMUM_RATIO = "MAXIMUM_RATIO"
    MEAN_RATIO = "MEAN_RATIO"
    MINIMUM_RATIO = "MINIMUM_RATIO"
    RELATIVE_ENTROPY = "RELATIVE_ENTROPY"
    STANDARD_DEVIATION_RATIO = "STANDARD_DEVIATION_RATIO"
    SUM_RATIO = "SUM_RATIO"


class NumericMetric(str, Enum):
    MAX = "MAX"
    MEAN = "MEAN"
    MIN = "MIN"
    STD = "STD"
    SUM = "SUM"


class RelativeTimeMetric(str, Enum):
    MAXIMUM_DIFFERENCE = "MAXIMUM_DIFFERENCE"
    MEAN_DIFFERENCE = "MEAN_DIFFERENCE"
    MINIMUM_DIFFERENCE = "MINIMUM_DIFFERENCE"


class RelativeVolumeMetric(str, Enum):
    COUNT_RATIO = "COUNT_RATIO"
    PERCENTAGE_RATIO = "PERCENTAGE_RATIO"


class Role(str, Enum):
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"


class Scope(str, Enum):
    GLOBAL = "GLOBAL"
    NAMESPACE = "NAMESPACE"
    SELF = "SELF"


class SortOrder(str, Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class SourcePollProgressStatus(str, Enum):
    FAILED = "FAILED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"


class SourceState(str, Enum):
    BACKFILLING = "BACKFILLING"
    IDLE = "IDLE"
    INIT = "INIT"
    PENDING_BACKFILL = "PENDING_BACKFILL"
    POLLING = "POLLING"
    RUNNING = "RUNNING"
    STARTING = "STARTING"
    STOPPING = "STOPPING"


class StreamingSourceMessageFormat(str, Enum):
    AVRO = "AVRO"
    JSON = "JSON"
    PROTOBUF = "PROTOBUF"


class StringOperator(str, Enum):
    CONTAINS = "CONTAINS"
    DOES_NOT_CONTAIN = "DOES_NOT_CONTAIN"
    ENDS_WITH = "ENDS_WITH"
    IS_EMPTY = "IS_EMPTY"
    IS_EXACTLY = "IS_EXACTLY"
    IS_NOT_EMPTY = "IS_NOT_EMPTY"
    REGEX = "REGEX"
    STARTS_WITH = "STARTS_WITH"


class TagOrigin(str, Enum):
    CATALOG_REFRESH = "CATALOG_REFRESH"
    DBT = "DBT"
    VALIDIO = "VALIDIO"


class UserDeleteErrorCode(str, Enum):
    UNKNOWN = "UNKNOWN"


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"


class UserUpdateErrorCode(str, Enum):
    UNKNOWN = "UNKNOWN"


class ValidatorState(str, Enum):
    BACKFILLING = "BACKFILLING"
    PENDING_BACKFILL = "PENDING_BACKFILL"
    PROCESSING = "PROCESSING"
    RUNNING = "RUNNING"


class VolumeMetric(str, Enum):
    COUNT = "COUNT"
    DUPLICATES_COUNT = "DUPLICATES_COUNT"
    DUPLICATES_PERCENTAGE = "DUPLICATES_PERCENTAGE"
    PERCENTAGE = "PERCENTAGE"
    UNIQUE_COUNT = "UNIQUE_COUNT"
    UNIQUE_PERCENTAGE = "UNIQUE_PERCENTAGE"


class WindowTimeUnit(str, Enum):
    DAY = "DAY"
    HOUR = "HOUR"
    MINUTE = "MINUTE"
    MONTH = "MONTH"
    WEEK = "WEEK"

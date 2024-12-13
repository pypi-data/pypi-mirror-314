"""Notification rule configuration."""

from enum import Enum
from typing import TYPE_CHECKING, Any

from validio_sdk.exception import ValidioError
from validio_sdk.graphql_client.enums import IncidentSeverity as LegacyIncidentSeverity
from validio_sdk.graphql_client.enums import IssueTypename as LegacyIssueTypename
from validio_sdk.resource._diffable import Diffable
from validio_sdk.resource._resource import Resource
from validio_sdk.resource._serde import (
    NODE_TYPE_FIELD_NAME,
    _api_create_input_params,
    _api_update_input_params,
    _encode_resource,
    get_config_node,
)
from validio_sdk.resource.channels import Channel
from validio_sdk.resource.sources import Source

if TYPE_CHECKING:
    from validio_sdk.resource._diff import DiffContext


class IncidentSeverity(str, Enum):
    """Severity of an incident severity condition."""

    HIGH = "HIGH"
    LOW = "LOW"
    MEDIUM = "MEDIUM"


class IssueTypename(str, Enum):
    """Name of issue type."""

    GenericSourceError = "GenericSourceError"
    SchemaChangeSourceError = "SchemaChangeSourceError"
    SegmentLimitExceededSourceError = "SegmentLimitExceededSourceError"
    ValidatorIncident = "ValidatorIncident"


class Conditions(Diffable):
    """Conditions used for notification rules."""

    def __init__(
        self,
        owner_condition: "OwnerNotificationRuleCondition | None" = None,
        segment_conditions: list["SegmentNotificationRuleCondition"] | None = None,
        severity_condition: "SeverityNotificationRuleCondition | None" = None,
        source_condition: "SourceNotificationRuleCondition | None" = None,
        tag_conditions: list["TagNotificationRuleCondition"] | None = None,
        type_condition: "TypeNotificationRuleCondition | None" = None,
    ) -> None:
        """Constructor."""
        self._node_type = self.__class__.__name__

        self.owner_condition = owner_condition
        self.segment_conditions = segment_conditions
        self.severity_condition = severity_condition
        self.source_condition = source_condition
        self.tag_conditions = tag_conditions
        self.type_condition = type_condition

    def _immutable_fields(self) -> set[str]:
        return set()

    def _mutable_fields(self) -> set[str]:
        return set()

    def _nested_objects(self) -> dict[str, Diffable | list[Diffable] | None]:
        # For some reason mypy doesn't recognize <Type>Condition -> Condition ->
        # Diffable as fulfiling the Diffable type.
        objects: dict[str, Diffable | list[Diffable] | None] = {  # type: ignore
            "owner_condition": self.owner_condition,
            "segment_conditions": self.segment_conditions,  # type: ignore
            "severity_condition": self.severity_condition,
            "source_condition": self.source_condition,
            "tag_conditions": self.tag_conditions,  # type: ignore
            "type_condition": self.type_condition,
        }

        return objects

    def _encode(self) -> dict[str, object]:
        return self.__dict__

    @staticmethod
    def _decode(ctx: "DiffContext", obj: dict[str, Any]) -> "Conditions":
        cls = eval(obj[NODE_TYPE_FIELD_NAME])

        args = {}
        for k, v in obj.items():
            if v is None:
                continue

            if k == NODE_TYPE_FIELD_NAME:
                continue

            if isinstance(v, list):
                values = []
                for value_element in v:
                    condition_cls = eval(value_element[NODE_TYPE_FIELD_NAME])
                    values.append(condition_cls._decode(ctx, value_element))

                args[k] = values
            else:
                condition_cls = eval(v[NODE_TYPE_FIELD_NAME])
                args[k] = condition_cls._decode(ctx, v)

        return cls(**args)

    def _create_input(self, ctx: "DiffContext") -> dict[str, Any]:
        conditions: dict[str, Any] = {}
        if self.owner_condition is not None:
            conditions["ownerCondition"] = {"owners": self.owner_condition.owners}

        if self.severity_condition is not None:
            conditions["severityCondition"] = {
                "severities": [s.value for s in self.severity_condition.severities]
            }

        if self.source_condition is not None:
            conditions["sourceCondition"] = {
                "sources": [
                    ctx.sources[source_name]._must_id()
                    for source_name in self.source_condition.sources
                ]
            }

        if self.type_condition is not None:
            conditions["typeCondition"] = {"types": self.type_condition.types}

        if self.segment_conditions is not None:
            conditions["segmentConditions"] = [
                {
                    "segments": [
                        {"field": k, "value": v}
                        for k, v in segment_condition.segments.items()
                    ]
                }
                for segment_condition in self.segment_conditions
            ]

        if self.tag_conditions is not None:
            conditions["tagConditions"] = [
                {
                    "tags": [
                        {"key": k, "value": v} for k, v in tag_condition.tags.items()
                    ]
                }
                for tag_condition in self.tag_conditions
            ]

        return conditions

    def _api_create_input(self, ctx: "DiffContext") -> dict[str, Any]:
        return self._create_input(ctx)

    def _api_update_input(self, ctx: "DiffContext") -> dict[str, Any]:
        return self._create_input(ctx)

    @classmethod
    def _new_from_api(
        cls: type["Conditions"],
        ctx: "DiffContext",
        api_conditions: list[dict[str, Any]],
    ) -> "Conditions":
        """
        Create a new Conditions from API response.

        Input for creating and updating conditions for a notification rules in
        the API is a typed struct with fields for each condition type. Some of
        them might occur several times and is a list where others are just plain
        values.

        Output from the API however lists conditions as an array with elements
        being one conditions per row. This includes both across different
        condition types, f.ex. source conditions and type conditions are two
        different elements, but also for each condition that is represented as a
        list on the input, f.ex. each tag or segment will be returned as
        separate elements.

        This method will convert the API response and the expanded array for
        conditions to a `Conditions` type which is the same as the
        representation for create and update.
        """
        conditions = cls()
        for condition in api_conditions:
            match condition["__typename"]:
                case "OwnerNotificationRuleCondition":
                    conditions.owner_condition = OwnerNotificationRuleCondition(
                        owners=[x["id"] for x in condition["config"]["owners"]]
                    )
                case "SegmentNotificationRuleCondition":
                    if conditions.segment_conditions is None:
                        conditions.segment_conditions = []

                    conditions.segment_conditions.append(
                        SegmentNotificationRuleCondition(
                            segments={
                                x["field"]: x["value"]
                                for x in condition["config"]["segments"]
                            }
                        )
                    )
                case "SeverityNotificationRuleCondition":
                    conditions.severity_condition = SeverityNotificationRuleCondition(
                        severities=condition["config"]["severities"]
                    )
                case "SourceNotificationRuleCondition":
                    sources = [
                        ctx.sources[source["resourceName"]]
                        for source in condition["config"]["sources"]
                        if source is not None and source["resourceName"] in ctx.sources
                    ]

                    conditions.source_condition = SourceNotificationRuleCondition(
                        sources=sources
                    )
                case "TagNotificationRuleCondition":
                    if conditions.tag_conditions is None:
                        conditions.tag_conditions = []

                    conditions.tag_conditions.append(
                        TagNotificationRuleCondition(
                            tags={
                                x["key"]: x["value"]
                                for x in condition["config"]["tags"]
                            }
                        )
                    )
                case "TypeNotificationRuleCondition":
                    conditions.type_condition = TypeNotificationRuleCondition(
                        types=[IssueTypename(x) for x in condition["config"]["types"]]
                    )

        return conditions


class NotificationRuleCondition(Diffable):
    """A condition for notification rules."""

    def __init__(self) -> None:
        """Base class for all notification rule conditions."""
        self._node_type = self.__class__.__name__

    def _immutable_fields(self) -> set[str]:
        return set()

    def _mutable_fields(self) -> set[str]:
        return set()

    def _nested_objects(self) -> dict[str, Diffable | list[Diffable] | None]:
        return {}

    def _encode(self) -> dict[str, Any]:
        return self.__dict__

    @staticmethod
    def _decode(_: "DiffContext", obj: dict[str, Any]) -> "NotificationRuleCondition":
        cls = eval(obj[NODE_TYPE_FIELD_NAME])
        return cls(**{k: v for k, v in obj.items() if k != NODE_TYPE_FIELD_NAME})


class OwnerNotificationRuleCondition(NotificationRuleCondition):
    """A condition for owners."""

    def __init__(self, owners: list[str]):
        """
        Constructor.

        :param owners: User IDs in uuid format. Will send notification for
        reasources owned by these users.
        """
        super().__init__()

        from uuid import UUID

        # Ensure we only try to work with valid UUIDs.
        for owner in owners:
            try:
                UUID(owner)
            except ValueError:
                raise ValidioError("owner must be id of type uuid")

        self.owners = owners
        self.owners.sort()

    def _mutable_fields(self) -> set[str]:
        return {"owners"}


class SegmentNotificationRuleCondition(NotificationRuleCondition):
    """A condition for segments."""

    def __init__(self, segments: dict[str, str]):
        """
        Constructor.

        :param segments: Key value pairs of field and field values for segments
        to send notifications for.
        """
        super().__init__()
        self.segments = segments

    def _mutable_fields(self) -> set[str]:
        return {"segments"}


class SeverityNotificationRuleCondition(NotificationRuleCondition):
    """A condition for severity."""

    def __init__(
        self,
        severities: list[IncidentSeverity] | list[LegacyIncidentSeverity],
    ):
        """
        Constructor.

        :param severities: List of severities to send notifications for.
        """
        super().__init__()
        self.severities = [
            severity
            if isinstance(severity, (IncidentSeverity, LegacyIncidentSeverity))
            else IncidentSeverity(severity)
            for severity in severities
        ]
        self.severities.sort()

    def _mutable_fields(self) -> set[str]:
        return {"severities"}


class SourceNotificationRuleCondition(NotificationRuleCondition):
    """A condition for sources."""

    def __init__(self, sources: list[Source]):
        """
        Constructor.

        :param sources: List of sources to send notifications for.
        """
        super().__init__()
        self.sources = [source.name for source in sources]
        self.sources.sort()

    def _mutable_fields(self) -> set[str]:
        return {"sources"}

    @staticmethod
    def _decode(
        ctx: "DiffContext", obj: dict[str, Any]
    ) -> "SourceNotificationRuleCondition":
        sources = [ctx.sources[source] for source in obj["sources"]]
        return SourceNotificationRuleCondition(sources=sources)


class TagNotificationRuleCondition(NotificationRuleCondition):
    """A condition for tags."""

    def __init__(self, tags: dict[str, str | None]):
        """
        Constructor.

        :param tags: Key value pairs of tags to send notifications for.
        """
        super().__init__()
        self.tags = tags

    def _mutable_fields(self) -> set[str]:
        return {"tags"}


class TypeNotificationRuleCondition(NotificationRuleCondition):
    """A condition for sources."""

    def __init__(
        self,
        types: list[IssueTypename] | list[LegacyIssueTypename],
    ):
        """
        Constructor.

        :param types: A list of event types to send notifications for.
        """
        super().__init__()
        self.types = [
            type_
            if isinstance(type_, (IssueTypename, LegacyIssueTypename))
            else IssueTypename(type_)
            for type_ in types
        ]
        self.types.sort()

    def _mutable_fields(self) -> set[str]:
        return {"types"}


class NotificationRule(Resource):
    """
    A notification rule.

    https://docs.validio.io/docs/notifications
    """

    def __init__(
        self,
        name: str,
        channel: Channel,
        conditions: Conditions | None = None,
        display_name: str | None = None,
        ignore_changes: bool = False,
    ):
        """
        Constructor.

        :param name: Unique resource name assigned to the window
        :param channel: The channel to attach the rule to
        :param conditions: List of conditions for the notification rule.
        :param display_name: Human-readable name for the channel. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored.
        """
        super().__init__(
            name=name,
            display_name=display_name,
            ignore_changes=ignore_changes,
            __internal__=channel._resource_graph,
        )

        self.channel_name = channel.name

        # If conditions wasn't set, set it to an empty `Conditions` with all
        # fields to `None` to not have to account for `None`-ness of the field.
        self.conditions = conditions or Conditions()

        if self.conditions.severity_condition is not None and any(
            isinstance(x, LegacyIncidentSeverity)
            for x in self.conditions.severity_condition.severities
        ):
            self.add_enum_deprecation(self.conditions.severity_condition.severities[0])

        if self.conditions.type_condition is not None and any(
            isinstance(x, LegacyIssueTypename)
            for x in self.conditions.type_condition.types
        ):
            self.add_enum_deprecation(self.conditions.type_condition.types[0])

        channel.add(self.name, self)

    def _nested_objects(self) -> dict[str, Diffable | list[Diffable] | None]:
        objects: dict[str, Diffable | list[Diffable] | None] = {
            "conditions": self.conditions,
        }

        return objects

    def _immutable_fields(self) -> set[str]:
        return {"channel_name"}

    def resource_class_name(self) -> str:
        """Returns the base class name."""
        return "NotificationRule"

    def _api_create_response_field_name(self) -> str:
        return "notificationRule"

    def _api_create_input(self, _namespace: str, ctx: "DiffContext") -> Any:
        return _api_create_input_params(
            self,
            overrides={
                "channelId": ctx.channels[self.channel_name]._must_id(),
                "conditions": self.conditions._api_create_input(ctx),
            },
            skip_fields={"sources", "notificationTypenames"},
        )

    def _api_update_input(self, _namespace: str, ctx: "DiffContext") -> Any:
        return _api_update_input_params(
            self,
            overrides={
                "conditions": self.conditions._api_update_input(ctx),
            },
        )

    def _api_delete_method_name(self) -> str:
        # Notification rules are not deleted in bulk.
        return "notificationRuleDelete"

    def _api_delete_arguments(self) -> dict[str, str]:
        return {"input": f"{self.resource_class_name()}DeleteInput!"}

    def _api_delete_input(self) -> Any:
        return {"input": {"id": self._must_id()}}

    def _encode(self) -> dict[str, object]:
        # Drop fields here that are not part of the constructor for when
        # we deserialize back. They will be reinitialized by the constructor.
        return _encode_resource(self, skip_fields={"channel_name"})

    @staticmethod
    def _decode(
        ctx: "DiffContext",
        channel: Channel,
        obj: dict[str, Any],
    ) -> "NotificationRule":
        args: dict[str, Any] = get_config_node(obj)

        conditions = Conditions._decode(ctx, args["conditions"])

        return NotificationRule(
            **{
                **args,
                "channel": channel,
                "conditions": conditions,
            }
        )  # type: ignore

"""Notification Channels."""

from typing import TYPE_CHECKING, Any, cast

from camel_converter import to_camel

from validio_sdk.resource._errors import ManifestConfigurationError
from validio_sdk.resource._resource import Resource, ResourceGraph
from validio_sdk.resource._resource_graph import RESOURCE_GRAPH
from validio_sdk.resource._serde import (
    _api_create_input_params,
    _encode_resource,
    get_children_node,
    get_config_node,
    with_resource_graph_info,
)

if TYPE_CHECKING:
    from validio_sdk.resource._diff import DiffContext


class Channel(Resource):
    """A notification channel configuration.

    https://docs.validio.io/docs/channels
    """

    def __init__(
        self,
        name: str,
        display_name: str | None,
        ignore_changes: bool = False,
        __internal__: ResourceGraph | None = None,
    ) -> None:
        """
        Constructor.

        :param name: Unique resource name assigned to the destination
        :param display_name: Human-readable name for the channel. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored.
        :param __internal__: Should be left ignored. This is for internal usage only.
        """
        # Channels are at the root sub-graphs.
        g: ResourceGraph = __internal__ or RESOURCE_GRAPH
        super().__init__(
            name=name,
            display_name=display_name,
            ignore_changes=ignore_changes,
            __internal__=g,
        )

        self._resource_graph: ResourceGraph = g
        self._resource_graph._add_root(self)

    def _deprecated_secret_fields(self) -> set[str]:
        """Fields that are not supported when calling the secrets changed endpoint.

        :return: Set of secret fields that are deprecated
        """
        return set({})

    def _immutable_fields(self) -> set[str]:
        return set({})

    def _all_fields(self) -> set[str]:
        return {
            *super()._all_fields(),
            *self._secret_fields(),
        }

    def resource_class_name(self) -> str:
        """Returns the base class name."""
        return "Channel"

    def _encode(self) -> dict[str, object]:
        return _encode_resource(self)

    def _api_delete_method_name(self) -> str:
        # Channels are not deleted in bulk like other resources so we can't use
        # the parent method which is in plural. Instead of
        # `<ChannelType>sDelete` the method is called `<ChannelType>Delete`.
        return f"{self.resource_class_name().lower()}Delete"

    def _api_delete_arguments(self) -> dict[str, str]:
        return {"input": f"{self.resource_class_name()}DeleteInput!"}

    def _api_delete_input(self) -> Any:
        return {"input": {"id": self._must_id()}}

    def _api_create_input(self, namespace: str, _: "DiffContext") -> Any:
        return _api_create_input_params(self, overrides={"namespaceId": namespace})

    @staticmethod
    def _decode(
        ctx: "DiffContext",
        cls: type,
        obj: dict[str, dict[str, object]],
        g: ResourceGraph,
    ) -> "Channel":
        from validio_sdk.resource.notification_rules import NotificationRule

        args = get_config_node(obj)

        channel = cls(**with_resource_graph_info(args, g))

        # Decode notification rules
        children_obj = cast(dict[str, dict[str, object]], get_children_node(obj))
        notification_rules_obj = cast(
            dict[str, dict[str, object]],
            (
                children_obj[NotificationRule.__name__]
                if NotificationRule.__name__ in children_obj
                else {}
            ),
        )

        notification_rules = {}
        for rule_name, value in notification_rules_obj.items():
            rule = NotificationRule._decode(ctx, channel, value)
            notification_rules[rule_name] = rule
            ctx.notification_rules[rule_name] = rule

        if len(notification_rules) > 0:
            channel._children[NotificationRule.__name__] = cast(
                dict[str, Resource], notification_rules
            )

        return channel

    def _api_secret_change_response_fields(self) -> set[str]:
        fields = super()._api_secret_change_response_fields()
        deprecated_fields = [
            to_camel(secret_field) for secret_field in self._deprecated_secret_fields()
        ]
        return set(fields).difference(deprecated_fields)


class SlackChannel(Channel):
    """
    Configuration to send notifications to a Slack channel.

    https://docs.validio.io/docs/slack
    """

    def __init__(
        self,
        name: str,
        application_link_url: str,
        slack_channel_id: str | None = None,
        token: str | None = None,
        signing_secret: str | None = None,
        interactive_message_enabled: bool | None = None,
        webhook_url: str | None = None,
        timezone: str | None = None,
        display_name: str | None = None,
        ignore_changes: bool = False,
        __internal__: ResourceGraph | None = None,
    ):
        """
        Constructor.

        :param application_link_url: URL to your Validio application
            instance, used to send notifications.
        :param slack_channel_id: Slack channel ID to send to.
        :param token: Slack API token.
        :param signing_secret: Slack API signing secret.
        :param interactive_message_enabled: If interactive notification messages should
         be used.
        :param webhook_url: Webhook URL provided by Slack to the
            specified Slack channel. (deprecated)
        :param timezone: Timezone to display timestamps in the notifications in.
          (deprecated)
        :param display_name: Human-readable name for the channel. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored.
        """
        super().__init__(
            name=name,
            display_name=display_name,
            ignore_changes=ignore_changes,
            __internal__=__internal__,
        )
        self.application_link_url = application_link_url
        self.webhook_url = webhook_url
        self.slack_channel_id = slack_channel_id
        self.token = token
        self.signing_secret = signing_secret
        self.interactive_message_enabled = interactive_message_enabled

        if webhook_url and (
            slack_channel_id or token or signing_secret or interactive_message_enabled
        ):
            raise ManifestConfigurationError(
                f"invalid configuration for Slack channel {self.name}: either"
                " webhook_url or slack_channel_id, token, signing_secret and"
                " interactive_message_enabled can be used."
            )

        if timezone is None:
            timezone = "UTC"
        else:
            self.add_deprecation(
                "Timezone configuration is deprecated and "
                "support will be removed in a future release. "
                "Timestamps in notifications will be shown in UTC."
            )

        if webhook_url:
            self.add_field_deprecation("webhook_url")

        self.timezone = timezone

    def _secret_fields(self) -> set[str]:
        # If the webhook URL is set, we return an empty set so that the caller can
        # avoid calling the secrets changed endpoint as it's not supported
        return set({}) if self.webhook_url else {"signing_secret", "token"}

    def _immutable_fields(self) -> set[str]:
        return set({})

    def _mutable_fields(self) -> set[str]:
        return {
            *super()._mutable_fields(),
            *{
                "application_link_url",
                "slack_channel_id",
                "timezone",
                "interactive_message_enabled",
                *self._deprecated_secret_fields(),
            },
        }

    def _deprecated_secret_fields(self) -> set[str]:
        return {"webhook_url"}

    def _api_create_input(self, namespace: str, ctx: "DiffContext") -> Any:
        api_input = super()._api_create_input(namespace, ctx)
        if not self.webhook_url:
            del api_input["input"]["webhookUrl"]

        return api_input

    def _api_update_input(self, namespace: str, ctx: "DiffContext") -> Any:
        api_input = super()._api_update_input(namespace, ctx)
        if not self.webhook_url:
            del api_input["input"]["webhookUrl"]

        return api_input


class MsTeamsChannel(Channel):
    """
    Configuration to send notifications to a Microsoft Teams channel.

    https://docs.validio.io/docs/msteams
    """

    def __init__(
        self,
        name: str,
        application_link_url: str,
        ms_teams_channel_id: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        interactive_message_enabled: bool | None = None,
        webhook_url: str | None = None,
        timezone: str | None = None,
        display_name: str | None = None,
        ignore_changes: bool = False,
        __internal__: ResourceGraph | None = None,
    ):
        """
        Constructor.

        :param application_link_url: URL to your Validio application
            instance, used to send notifications.
        :param ms_teams_channel_id: Channel ID to send notifications to.
        :param client_id: Client ID for authentication.
        :param client_secret: Client secret for authentication.
        :param interactive_message_enabled: If interactive notification messages should
         be used.
        :param webhook_url: Webhook URL provided by Microsoft Teams to the
            specified channel. (deprecated)
        :param timezone: Timezone to display timestamps in the notifications in.
          (deprecated)
        :param display_name: Human-readable name for the channel. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored.
        """
        super().__init__(
            name=name,
            display_name=display_name,
            ignore_changes=ignore_changes,
            __internal__=__internal__,
        )
        self.application_link_url = application_link_url
        self.webhook_url = webhook_url
        self.ms_teams_channel_id = ms_teams_channel_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.interactive_message_enabled = interactive_message_enabled

        if webhook_url and (
            ms_teams_channel_id
            or client_id
            or client_secret
            or interactive_message_enabled
        ):
            raise ManifestConfigurationError(
                f"invalid configuration for MS Teams channel {self.name}: either"
                " webhook_url or ms_teams_channel_id, client_id, client_secret,"
                " and interactive_message_enabled can be used."
            )

        if timezone is None:
            timezone = "UTC"
        else:
            self.add_deprecation(
                "Timezone configuration is deprecated and "
                "support will be removed in a future release. "
                "Timestamps in notifications will be shown in UTC."
            )

        if webhook_url:
            self.add_field_deprecation("webhook_url")

        self.timezone = timezone

    def _secret_fields(self) -> set[str]:
        # If the webhook URL is set, we return an empty set so that the caller can
        # avoid calling the secrets changed endpoint as it's not supported
        return set({}) if self.webhook_url else {"client_id", "client_secret"}

    def _immutable_fields(self) -> set[str]:
        return set({})

    def _mutable_fields(self) -> set[str]:
        return {
            *super()._mutable_fields(),
            *{
                "application_link_url",
                "ms_teams_channel_id",
                "timezone",
                "interactive_message_enabled",
                *self._deprecated_secret_fields(),
            },
        }

    def _deprecated_secret_fields(self) -> set[str]:
        return {"webhook_url"}

    def _api_create_input(self, namespace: str, ctx: "DiffContext") -> Any:
        api_input = super()._api_create_input(namespace, ctx)
        if not self.webhook_url:
            del api_input["input"]["webhookUrl"]

        return api_input

    def _api_update_input(self, namespace: str, ctx: "DiffContext") -> Any:
        api_input = super()._api_update_input(namespace, ctx)
        if not self.webhook_url:
            del api_input["input"]["webhookUrl"]

        return api_input


class WebhookChannel(Channel):
    """
    Configuration to send notifications to a webhook.

    https://docs.validio.io/docs/webhooks
    """

    def __init__(
        self,
        name: str,
        application_link_url: str,
        webhook_url: str,
        auth_header: str | None,
        display_name: str | None = None,
        ignore_changes: bool = False,
        __internal__: ResourceGraph | None = None,
    ):
        """
        Constructor.

        :param application_link_url: URL to your Validio application
            instance, used to send notifications.
        :param webhook_url: Webhook URL to the specified HTTP endpoint.
        :param auth_header: Signature to include in the authorization
            header sent to the HTTP endpoint.
        :param display_name: Human-readable name for the channel. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored.
        """
        super().__init__(
            name=name,
            display_name=display_name,
            ignore_changes=ignore_changes,
            __internal__=__internal__,
        )
        self.application_link_url = application_link_url
        self.webhook_url = webhook_url
        self.auth_header = auth_header

    def _secret_fields(self) -> set[str]:
        return {"auth_header"}

    def _immutable_fields(self) -> set[str]:
        return set({})

    def _mutable_fields(self) -> set[str]:
        return {
            *super()._mutable_fields(),
            *{"application_link_url", "webhook_url"},
        }

from datetime import datetime
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel


class ListChannels(BaseModel):
    channels_list: List[
        Annotated[
            Union[
                "ListChannelsChannelsListChannel",
                "ListChannelsChannelsListMsTeamsChannel",
                "ListChannelsChannelsListSlackChannel",
                "ListChannelsChannelsListWebhookChannel",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="channelsList")


class ListChannelsChannelsListChannel(BaseModel):
    typename__: Literal["Channel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListChannelsChannelsListChannelNamespace"
    notification_rules: List["ListChannelsChannelsListChannelNotificationRules"] = (
        Field(alias="notificationRules")
    )


class ListChannelsChannelsListChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class ListChannelsChannelsListChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class ListChannelsChannelsListMsTeamsChannel(BaseModel):
    typename__: Literal["MsTeamsChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListChannelsChannelsListMsTeamsChannelNamespace"
    notification_rules: List[
        "ListChannelsChannelsListMsTeamsChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "ListChannelsChannelsListMsTeamsChannelConfig"


class ListChannelsChannelsListMsTeamsChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class ListChannelsChannelsListMsTeamsChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class ListChannelsChannelsListMsTeamsChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")
    ms_teams_channel_id: Optional[str] = Field(alias="msTeamsChannelId")
    interactive_message_enabled: bool = Field(alias="interactiveMessageEnabled")


class ListChannelsChannelsListSlackChannel(BaseModel):
    typename__: Literal["SlackChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListChannelsChannelsListSlackChannelNamespace"
    notification_rules: List[
        "ListChannelsChannelsListSlackChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "ListChannelsChannelsListSlackChannelConfig"


class ListChannelsChannelsListSlackChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class ListChannelsChannelsListSlackChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class ListChannelsChannelsListSlackChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")
    slack_channel_id: Optional[str] = Field(alias="slackChannelId")
    interactive_message_enabled: bool = Field(alias="interactiveMessageEnabled")


class ListChannelsChannelsListWebhookChannel(BaseModel):
    typename__: Literal["WebhookChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListChannelsChannelsListWebhookChannelNamespace"
    notification_rules: List[
        "ListChannelsChannelsListWebhookChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "ListChannelsChannelsListWebhookChannelConfig"


class ListChannelsChannelsListWebhookChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class ListChannelsChannelsListWebhookChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class ListChannelsChannelsListWebhookChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    application_link_url: str = Field(alias="applicationLinkUrl")
    auth_header: Optional[str] = Field(alias="authHeader")


ListChannels.model_rebuild()
ListChannelsChannelsListChannel.model_rebuild()
ListChannelsChannelsListMsTeamsChannel.model_rebuild()
ListChannelsChannelsListSlackChannel.model_rebuild()
ListChannelsChannelsListWebhookChannel.model_rebuild()

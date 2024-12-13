from datetime import datetime
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel


class GetChannelByResourceName(BaseModel):
    channel_by_resource_name: Optional[
        Annotated[
            Union[
                "GetChannelByResourceNameChannelByResourceNameChannel",
                "GetChannelByResourceNameChannelByResourceNameMsTeamsChannel",
                "GetChannelByResourceNameChannelByResourceNameSlackChannel",
                "GetChannelByResourceNameChannelByResourceNameWebhookChannel",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="channelByResourceName")


class GetChannelByResourceNameChannelByResourceNameChannel(BaseModel):
    typename__: Literal["Channel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetChannelByResourceNameChannelByResourceNameChannelNamespace"
    notification_rules: List[
        "GetChannelByResourceNameChannelByResourceNameChannelNotificationRules"
    ] = Field(alias="notificationRules")


class GetChannelByResourceNameChannelByResourceNameChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class GetChannelByResourceNameChannelByResourceNameChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class GetChannelByResourceNameChannelByResourceNameMsTeamsChannel(BaseModel):
    typename__: Literal["MsTeamsChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetChannelByResourceNameChannelByResourceNameMsTeamsChannelNamespace"
    notification_rules: List[
        "GetChannelByResourceNameChannelByResourceNameMsTeamsChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "GetChannelByResourceNameChannelByResourceNameMsTeamsChannelConfig"


class GetChannelByResourceNameChannelByResourceNameMsTeamsChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class GetChannelByResourceNameChannelByResourceNameMsTeamsChannelNotificationRules(
    BaseModel
):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class GetChannelByResourceNameChannelByResourceNameMsTeamsChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")
    ms_teams_channel_id: Optional[str] = Field(alias="msTeamsChannelId")
    interactive_message_enabled: bool = Field(alias="interactiveMessageEnabled")


class GetChannelByResourceNameChannelByResourceNameSlackChannel(BaseModel):
    typename__: Literal["SlackChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetChannelByResourceNameChannelByResourceNameSlackChannelNamespace"
    notification_rules: List[
        "GetChannelByResourceNameChannelByResourceNameSlackChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "GetChannelByResourceNameChannelByResourceNameSlackChannelConfig"


class GetChannelByResourceNameChannelByResourceNameSlackChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class GetChannelByResourceNameChannelByResourceNameSlackChannelNotificationRules(
    BaseModel
):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class GetChannelByResourceNameChannelByResourceNameSlackChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")
    slack_channel_id: Optional[str] = Field(alias="slackChannelId")
    interactive_message_enabled: bool = Field(alias="interactiveMessageEnabled")


class GetChannelByResourceNameChannelByResourceNameWebhookChannel(BaseModel):
    typename__: Literal["WebhookChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetChannelByResourceNameChannelByResourceNameWebhookChannelNamespace"
    notification_rules: List[
        "GetChannelByResourceNameChannelByResourceNameWebhookChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "GetChannelByResourceNameChannelByResourceNameWebhookChannelConfig"


class GetChannelByResourceNameChannelByResourceNameWebhookChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class GetChannelByResourceNameChannelByResourceNameWebhookChannelNotificationRules(
    BaseModel
):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class GetChannelByResourceNameChannelByResourceNameWebhookChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    application_link_url: str = Field(alias="applicationLinkUrl")
    auth_header: Optional[str] = Field(alias="authHeader")


GetChannelByResourceName.model_rebuild()
GetChannelByResourceNameChannelByResourceNameChannel.model_rebuild()
GetChannelByResourceNameChannelByResourceNameMsTeamsChannel.model_rebuild()
GetChannelByResourceNameChannelByResourceNameSlackChannel.model_rebuild()
GetChannelByResourceNameChannelByResourceNameWebhookChannel.model_rebuild()

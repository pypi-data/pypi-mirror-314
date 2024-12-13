from pydantic import Field

from .base_model import BaseModel
from .fragments import ChannelUpdate


class UpdateWebhookChannel(BaseModel):
    webhook_channel_update: "UpdateWebhookChannelWebhookChannelUpdate" = Field(
        alias="webhookChannelUpdate"
    )


class UpdateWebhookChannelWebhookChannelUpdate(ChannelUpdate):
    pass


UpdateWebhookChannel.model_rebuild()

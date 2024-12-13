from pydantic import Field

from .base_model import BaseModel
from .fragments import ChannelUpdate


class UpdateSlackChannel(BaseModel):
    slack_channel_update: "UpdateSlackChannelSlackChannelUpdate" = Field(
        alias="slackChannelUpdate"
    )


class UpdateSlackChannelSlackChannelUpdate(ChannelUpdate):
    pass


UpdateSlackChannel.model_rebuild()

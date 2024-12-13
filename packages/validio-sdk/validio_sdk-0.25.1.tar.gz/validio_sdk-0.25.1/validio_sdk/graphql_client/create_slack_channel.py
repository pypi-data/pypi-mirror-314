from pydantic import Field

from .base_model import BaseModel
from .fragments import ChannelCreation


class CreateSlackChannel(BaseModel):
    slack_channel_create: "CreateSlackChannelSlackChannelCreate" = Field(
        alias="slackChannelCreate"
    )


class CreateSlackChannelSlackChannelCreate(ChannelCreation):
    pass


CreateSlackChannel.model_rebuild()

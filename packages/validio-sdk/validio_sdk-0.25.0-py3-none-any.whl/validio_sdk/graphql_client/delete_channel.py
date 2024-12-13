from pydantic import Field

from .base_model import BaseModel
from .fragments import ChannelDeletion


class DeleteChannel(BaseModel):
    channel_delete: "DeleteChannelChannelDelete" = Field(alias="channelDelete")


class DeleteChannelChannelDelete(ChannelDeletion):
    pass


DeleteChannel.model_rebuild()

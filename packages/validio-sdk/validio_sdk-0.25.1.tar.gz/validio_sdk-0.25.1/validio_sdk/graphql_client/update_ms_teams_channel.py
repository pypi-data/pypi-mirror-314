from pydantic import Field

from .base_model import BaseModel
from .fragments import ChannelUpdate


class UpdateMsTeamsChannel(BaseModel):
    ms_teams_channel_update: "UpdateMsTeamsChannelMsTeamsChannelUpdate" = Field(
        alias="msTeamsChannelUpdate"
    )


class UpdateMsTeamsChannelMsTeamsChannelUpdate(ChannelUpdate):
    pass


UpdateMsTeamsChannel.model_rebuild()

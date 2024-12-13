from pydantic import Field

from .base_model import BaseModel
from .fragments import ChannelCreation


class CreateMsTeamsChannel(BaseModel):
    ms_teams_channel_create: "CreateMsTeamsChannelMsTeamsChannelCreate" = Field(
        alias="msTeamsChannelCreate"
    )


class CreateMsTeamsChannelMsTeamsChannelCreate(ChannelCreation):
    pass


CreateMsTeamsChannel.model_rebuild()

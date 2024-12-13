from pydantic import Field

from .base_model import BaseModel
from .fragments import NamespaceUpdate


class UpdateChannelNamespace(BaseModel):
    channel_namespace_update: "UpdateChannelNamespaceChannelNamespaceUpdate" = Field(
        alias="channelNamespaceUpdate"
    )


class UpdateChannelNamespaceChannelNamespaceUpdate(NamespaceUpdate):
    pass


UpdateChannelNamespace.model_rebuild()

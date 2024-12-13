from typing import Optional

from .base_model import BaseModel
from .fragments import NamespaceDetailsWithFullAvatar


class GetNamespace(BaseModel):
    namespace: Optional["GetNamespaceNamespace"]


class GetNamespaceNamespace(NamespaceDetailsWithFullAvatar):
    pass


GetNamespace.model_rebuild()

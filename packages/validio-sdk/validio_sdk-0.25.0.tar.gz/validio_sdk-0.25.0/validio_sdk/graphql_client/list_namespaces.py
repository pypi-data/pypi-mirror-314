from typing import List

from .base_model import BaseModel
from .fragments import NamespaceDetails


class ListNamespaces(BaseModel):
    namespaces: List["ListNamespacesNamespaces"]


class ListNamespacesNamespaces(NamespaceDetails):
    pass


ListNamespaces.model_rebuild()

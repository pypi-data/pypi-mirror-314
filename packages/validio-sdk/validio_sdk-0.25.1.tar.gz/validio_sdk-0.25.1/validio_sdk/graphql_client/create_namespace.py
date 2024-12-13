from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails, NamespaceDetails


class CreateNamespace(BaseModel):
    namespace_create: "CreateNamespaceNamespaceCreate" = Field(alias="namespaceCreate")


class CreateNamespaceNamespaceCreate(BaseModel):
    errors: List["CreateNamespaceNamespaceCreateErrors"]
    namespace: Optional["CreateNamespaceNamespaceCreateNamespace"]


class CreateNamespaceNamespaceCreateErrors(ErrorDetails):
    pass


class CreateNamespaceNamespaceCreateNamespace(NamespaceDetails):
    pass


CreateNamespace.model_rebuild()
CreateNamespaceNamespaceCreate.model_rebuild()

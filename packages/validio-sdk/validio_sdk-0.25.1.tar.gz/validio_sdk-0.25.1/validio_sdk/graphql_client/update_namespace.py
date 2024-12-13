from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails, NamespaceDetails


class UpdateNamespace(BaseModel):
    namespace_update: "UpdateNamespaceNamespaceUpdate" = Field(alias="namespaceUpdate")


class UpdateNamespaceNamespaceUpdate(BaseModel):
    errors: List["UpdateNamespaceNamespaceUpdateErrors"]
    namespace: Optional["UpdateNamespaceNamespaceUpdateNamespace"]


class UpdateNamespaceNamespaceUpdateErrors(ErrorDetails):
    pass


class UpdateNamespaceNamespaceUpdateNamespace(NamespaceDetails):
    pass


UpdateNamespace.model_rebuild()
UpdateNamespaceNamespaceUpdate.model_rebuild()

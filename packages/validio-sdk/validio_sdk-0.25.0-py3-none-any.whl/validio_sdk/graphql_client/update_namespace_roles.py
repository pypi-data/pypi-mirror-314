from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails, NamespaceDetails


class UpdateNamespaceRoles(BaseModel):
    namespace_roles_update: "UpdateNamespaceRolesNamespaceRolesUpdate" = Field(
        alias="namespaceRolesUpdate"
    )


class UpdateNamespaceRolesNamespaceRolesUpdate(BaseModel):
    errors: List["UpdateNamespaceRolesNamespaceRolesUpdateErrors"]
    namespace: Optional["UpdateNamespaceRolesNamespaceRolesUpdateNamespace"]


class UpdateNamespaceRolesNamespaceRolesUpdateErrors(ErrorDetails):
    pass


class UpdateNamespaceRolesNamespaceRolesUpdateNamespace(NamespaceDetails):
    pass


UpdateNamespaceRoles.model_rebuild()
UpdateNamespaceRolesNamespaceRolesUpdate.model_rebuild()

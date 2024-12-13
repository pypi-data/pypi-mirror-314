from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails, NamespaceDetails


class RevokeNamespaceRoles(BaseModel):
    namespace_roles_revoke: "RevokeNamespaceRolesNamespaceRolesRevoke" = Field(
        alias="namespaceRolesRevoke"
    )


class RevokeNamespaceRolesNamespaceRolesRevoke(BaseModel):
    errors: List["RevokeNamespaceRolesNamespaceRolesRevokeErrors"]
    namespace: Optional["RevokeNamespaceRolesNamespaceRolesRevokeNamespace"]


class RevokeNamespaceRolesNamespaceRolesRevokeErrors(ErrorDetails):
    pass


class RevokeNamespaceRolesNamespaceRolesRevokeNamespace(NamespaceDetails):
    pass


RevokeNamespaceRoles.model_rebuild()
RevokeNamespaceRolesNamespaceRolesRevoke.model_rebuild()

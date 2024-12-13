from typing import List

from pydantic import Field

from .base_model import BaseModel


class ListResourceNamespaces(BaseModel):
    resource_namespaces_list: List["ListResourceNamespacesResourceNamespacesList"] = (
        Field(alias="resourceNamespacesList")
    )


class ListResourceNamespacesResourceNamespacesList(BaseModel):
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")


ListResourceNamespaces.model_rebuild()

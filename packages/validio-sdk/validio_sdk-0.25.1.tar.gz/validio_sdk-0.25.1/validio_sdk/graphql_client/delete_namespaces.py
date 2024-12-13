from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteNamespaces(BaseModel):
    namespaces_delete: "DeleteNamespacesNamespacesDelete" = Field(
        alias="namespacesDelete"
    )


class DeleteNamespacesNamespacesDelete(BaseModel):
    errors: List["DeleteNamespacesNamespacesDeleteErrors"]


class DeleteNamespacesNamespacesDeleteErrors(ErrorDetails):
    pass


DeleteNamespaces.model_rebuild()
DeleteNamespacesNamespacesDelete.model_rebuild()

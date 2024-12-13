from pydantic import Field

from .base_model import BaseModel
from .fragments import IdentityDeletion


class DeleteIdentity(BaseModel):
    identity_delete: "DeleteIdentityIdentityDelete" = Field(alias="identityDelete")


class DeleteIdentityIdentityDelete(IdentityDeletion):
    pass


DeleteIdentity.model_rebuild()

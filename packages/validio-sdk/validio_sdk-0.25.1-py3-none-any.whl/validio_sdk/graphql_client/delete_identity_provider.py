from pydantic import Field

from .base_model import BaseModel
from .fragments import IdentityProviderDeletion


class DeleteIdentityProvider(BaseModel):
    identity_provider_delete: "DeleteIdentityProviderIdentityProviderDelete" = Field(
        alias="identityProviderDelete"
    )


class DeleteIdentityProviderIdentityProviderDelete(IdentityProviderDeletion):
    pass


DeleteIdentityProvider.model_rebuild()

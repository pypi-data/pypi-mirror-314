from pydantic import Field

from .base_model import BaseModel
from .fragments import IdentityProviderUpdate


class UpdateLocalIdentityProvider(BaseModel):
    local_identity_provider_update: (
        "UpdateLocalIdentityProviderLocalIdentityProviderUpdate"
    ) = Field(alias="localIdentityProviderUpdate")


class UpdateLocalIdentityProviderLocalIdentityProviderUpdate(IdentityProviderUpdate):
    pass


UpdateLocalIdentityProvider.model_rebuild()

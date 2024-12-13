from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class AddCatalogAssetTags(BaseModel):
    catalog_asset_tags_add: "AddCatalogAssetTagsCatalogAssetTagsAdd" = Field(
        alias="catalogAssetTagsAdd"
    )


class AddCatalogAssetTagsCatalogAssetTagsAdd(BaseModel):
    errors: List["AddCatalogAssetTagsCatalogAssetTagsAddErrors"]


class AddCatalogAssetTagsCatalogAssetTagsAddErrors(ErrorDetails):
    pass


AddCatalogAssetTags.model_rebuild()
AddCatalogAssetTagsCatalogAssetTagsAdd.model_rebuild()

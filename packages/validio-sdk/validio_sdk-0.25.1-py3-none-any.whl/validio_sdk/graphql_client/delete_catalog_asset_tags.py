from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteCatalogAssetTags(BaseModel):
    catalog_asset_tags_delete: "DeleteCatalogAssetTagsCatalogAssetTagsDelete" = Field(
        alias="catalogAssetTagsDelete"
    )


class DeleteCatalogAssetTagsCatalogAssetTagsDelete(BaseModel):
    errors: List["DeleteCatalogAssetTagsCatalogAssetTagsDeleteErrors"]


class DeleteCatalogAssetTagsCatalogAssetTagsDeleteErrors(ErrorDetails):
    pass


DeleteCatalogAssetTags.model_rebuild()
DeleteCatalogAssetTagsCatalogAssetTagsDelete.model_rebuild()

from pydantic import BaseModel, Field
from typing import List

from asset_tags_service.models.asset_tags import AssetTags


class AssetTagGroup(BaseModel):
    assetFqn: str
    tags: List[AssetTags]

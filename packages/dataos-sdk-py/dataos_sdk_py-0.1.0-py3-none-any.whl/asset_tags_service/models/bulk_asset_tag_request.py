from pydantic import BaseModel, Field
from typing import List, Optional

from asset_tags_service.models.asset_tag_assign_request import AssetTagAssignRequest
from asset_tags_service.models.asset_tag_remove_request import AssetTagRemoveRequest


class BulkAssetTagRequest(BaseModel):
    assign: Optional[List[AssetTagAssignRequest]] = Field(None, description="A list of AssetTagAssignRequest objects representing the tags to be assigned to assets.")
    remove: Optional[List[AssetTagRemoveRequest]] = Field(None, description="A list of AssetTagRemoveRequest objects representing the tags to be removed from assets.")

    class Builder:
        def __init__(self):
            self.assign = None
            self.remove = None

        def set_assign(self, assign: List[AssetTagAssignRequest]):
            self.assign = assign
            return self

        def set_remove(self, remove: List[AssetTagRemoveRequest]):
            self.remove = remove
            return self

        def build(self):
            return BulkAssetTagRequest(assign=self.assign, remove=self.remove)


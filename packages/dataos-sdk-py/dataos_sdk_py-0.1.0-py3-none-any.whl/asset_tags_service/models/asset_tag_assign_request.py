from pydantic import BaseModel


class AssetTagAssignRequest(BaseModel):
    assetType: str
    assetFqn: str
    tagFqn: str
    groupId: str

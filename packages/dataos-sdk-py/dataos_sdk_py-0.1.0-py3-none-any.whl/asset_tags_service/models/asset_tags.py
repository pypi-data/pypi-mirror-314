from pydantic import BaseModel, Field
from pydantic.fields import Optional


class AssetTags(BaseModel):
    assetType: str
    assetFqn: Optional[str]
    tagFqn: str
    groupId: str
    createdAt: str
    updatedAt: str
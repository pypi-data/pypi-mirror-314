from pydantic import BaseModel, Field

class AssetTagRemoveRequest(BaseModel):
    assetFqn: str
    tagFqn: str

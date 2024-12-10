from pydantic import BaseModel, Extra
from typing import Optional


class Links(BaseModel):
    self: Optional[str]
    tags: Optional[str]
    tokens: Optional[str]
    avatars: Optional[str]
    download_avatars: Optional[str]
    grants: Optional[str]
    policies: Optional[str]


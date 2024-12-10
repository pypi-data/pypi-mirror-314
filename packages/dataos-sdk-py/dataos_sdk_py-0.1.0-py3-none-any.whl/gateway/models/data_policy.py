from pydantic import BaseModel
from typing import List

from gateway.models.policy import Policy


class DataPolicy(BaseModel):
    actions: List[str]
    priority: int
    condition: str
    mask: bool
    filter: bool
    name: str
    version: str
    type: str
    tags: List[str]
    description: str
    owner: str
    layer: str
    policy: Policy
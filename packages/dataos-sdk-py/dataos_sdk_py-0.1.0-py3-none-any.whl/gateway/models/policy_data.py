from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from gateway.models.filter import Filter
from gateway.models.mask import Mask


class UserSelector(BaseModel):
    match: str
    tags: List[str]


class ColumnSelector(BaseModel):
    column: Optional[str]
    policyName: Optional[str]
    masks: Optional[List[str]]
    tags: Optional[List[str]]


class Selector(BaseModel):
    user: Optional[UserSelector]
    column: Optional[ColumnSelector]


class PolicyData(BaseModel):
    priority: int
    type: str
    selector: Optional[Selector]
    mask: Optional[Mask]
    filters: Optional[List[Filter]]
    name: Optional[str]
    description: Optional[str]
    depot: Optional[str]
    collection: Optional[str]
    dataset: Optional[str]

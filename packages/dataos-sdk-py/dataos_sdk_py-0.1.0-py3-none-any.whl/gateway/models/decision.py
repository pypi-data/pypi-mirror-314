from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from gateway.models.dataset import Dataset
from gateway.models.filter import Filter
from gateway.models.mask import Masks


class User(BaseModel):
    match: Optional[str] = None
    name: str
    tags: Optional[List[str]] = None


class Decision(BaseModel):
    dataset: Optional[Dataset] = None
    user: Optional[User] = None
    masks: Optional[Dict[str, Masks]] = None
    filter: Optional[Filter] = None

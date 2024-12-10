from pydantic import BaseModel, Field
from typing import Optional, List


class ValueFrom(BaseModel):
    user_attribute: str


class Filters(BaseModel):
    column: Optional[str] = None
    operator: Optional[str] = None
    value: Optional[str] = None
    valueFrom: Optional[ValueFrom] = None
    supportedDataTypes: Optional[List[str]] = None


class Filter(BaseModel):
    name: str
    owner: str
    priority: int
    filters: List[Filters] = None

from typing import List, Dict, Any
from pydantic import BaseModel


class Tag(BaseModel):
    labelType: str
    state: str
    tagFQN: str


class Column(BaseModel):
    name: str
    dataType: str
    tags: List[Tag] = None


class Service(BaseModel):
    id: str
    type: str
    name: str
    fullyQualifiedName: str
    deleted: bool
    href: str


class Dataset(BaseModel):
    id: str
    fullyQualifiedName: str
    name: str
    version: float
    updatedAt: int
    updatedBy: str
    href: str
    service: Service = None
    serviceType: str = None
    depot: str
    collection: str
    dataset: str
    tags: List[Tag] = None
    columns: List[Column] = None

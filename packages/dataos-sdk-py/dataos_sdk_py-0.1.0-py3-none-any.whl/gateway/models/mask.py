from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from pydantic.fields import Field


class MaskHash(BaseModel):
    algo: str


class MaskPassThrough(BaseModel):
    pass


class MaskBucketNumber(BaseModel):
    buckets: List[int]


class MaskBucketDate(BaseModel):
    precision: str


class MaskRandPattern(BaseModel):
    pattern: str


class MaskRandRegexify(BaseModel):
    pattern: str


class MaskRegexReplace(BaseModel):
    pattern: str
    replacement: str


class Mask(BaseModel):
    operator: str
    pass_through: Optional[MaskPassThrough]
    hash: Optional[MaskHash]
    redact: Optional[Dict[str, Any]]
    bucket_number: Optional[MaskBucketNumber]
    bucket_date: Optional[MaskBucketDate]
    rand_pattern: Optional[MaskRandPattern]
    rand_regexify: Optional[MaskRandRegexify]
    regex_replace: Optional[MaskRegexReplace]
    supported_data_types: Optional[List[str]] = Field(alias="supportedDataTypes")


class Masks(BaseModel):
    name: str
    owner: str
    priority: int
    mask: Mask

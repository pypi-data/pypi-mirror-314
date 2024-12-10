from pydantic import BaseModel
from typing import Optional


class Data(BaseModel,):
    key: Optional[str]
    base64Value: Optional[str]

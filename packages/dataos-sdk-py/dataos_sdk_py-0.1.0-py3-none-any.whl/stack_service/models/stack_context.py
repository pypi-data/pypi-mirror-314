from pydantic import BaseModel


class StackContext(BaseModel):
    contextId: str
    executionId: str
    properties: dict
    data: dict
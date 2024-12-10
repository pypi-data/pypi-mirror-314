from pydantic import BaseModel

from gateway.models.policy_data import PolicyData


class Policy(BaseModel):
    data: PolicyData

from pydantic import BaseModel, Field
from typing import Optional


class PChildBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=20, regex="^.+$")
    description: Optional[str] = Field(max_length=50, regex="^.+$")
    parent_id: Optional[int] = None


class PChildDB(PChildBase):
    id: int

from pydantic import BaseModel, Field
from typing import List, Optional

from schemas.child import PChildBase


class PParentBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=20, regex="^.+$")
    description: Optional[str] = Field(max_length=50, regex="^.+$")

    class Config:
        orm_mode = True


class PParentDB(PParentBase):
    id: int


class PParentChildren(PParentDB):
    children: List[PChildBase]


class PParentDBCount(PParentChildren):
    children_count: int

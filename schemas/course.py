from pydantic import BaseModel, Field
from typing import Optional


class PCourseBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=40, regex="^.+$")
    description: Optional[str] = Field(max_length=50, regex="^.+$")

    class Config:
        orm_mode = True


class PCourseDB(PCourseBase):
    id: int

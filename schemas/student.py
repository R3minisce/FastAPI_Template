from pydantic import BaseModel, Field
from typing import List

from config.parameters import PHONE_POLICY
from schemas.course import PCourseDB


class PStudentBase(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=40, regex="^.+$")
    last_name: str = Field(..., min_length=3, max_length=40, regex="^.+$")
    phone: str = Field(..., min_length=3, max_length=20,
                       regex=PHONE_POLICY)
    address: str = Field(..., min_length=3, max_length=255, regex="^.+$")

    class Config:
        orm_mode = True


class PStudentCoursesIDs(PStudentBase):
    courses_ids: List[int]


class PStudentDB(PStudentBase):
    id: int


""""
# Many to Many Relations
"""
class PStudentCourses(PStudentDB):
    courses: List[PCourseDB]


class PCourseStudents(PCourseDB):
    students: List[PStudentDB]

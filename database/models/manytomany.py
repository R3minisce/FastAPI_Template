from tortoise.exceptions import NoValuesFetched
from tortoise.models import Model
from tortoise import fields
from typing import List

from schemas.student import PStudentBase
from schemas.course import PCourseBase


class Student(Model):
    id = fields.IntField(pk=True, generated=True, index=True)
    first_name = fields.CharField(max_length=45, index=True)
    last_name = fields.CharField(max_length=45, index=True)
    phone = fields.CharField(max_length=20, index=True)
    address = fields.CharField(max_length=255, index=True)
    courses_list: fields.ManyToManyRelation["Course"]

    async def courses(self) -> List[PCourseBase]:
        try:
            return await self.courses_list.all()
        except NoValuesFetched:
            return -1

    class PydanticMeta:
        computed = ("courses_list",)


class Course(Model):
    id = fields.IntField(pk=True, generated=True, index=True)
    name = fields.CharField(max_length=25, index=True)
    description = fields.CharField(max_length=255, index=True)
    students_list: fields.ManyToManyRelation[Student] = fields.ManyToManyField('models.Student',
                                                                               related_name='courses_list',
                                                                               through='student_course')

    async def students(self) -> List[PStudentBase]:
        try:
            return await self.students_list.all()
        except NoValuesFetched:
            return -1

    class PydanticMeta:
        computed = ("students_list",)
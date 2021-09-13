from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.tortoise import paginate

from schemas.student import PStudentBase, PStudentCoursesIDs
from database.controllers import courses
from database.models.manytomany import Student


async def get_student(id_student: int) -> Student:
    obj = await Student.get(id=id_student).prefetch_related()
    obj.courses = await obj.courses()
    return obj


async def get_students() -> AbstractPage:
    return await paginate(Student.all())


async def create_student(student: PStudentCoursesIDs) -> Student:
    student_obj = PStudentBase(**student.dict(exclude_unset=True))
    obj = await Student.create(**student_obj.dict(exclude_unset=True))
    [await obj.courses_list.add(await courses.get_course(id)) for id in student.courses_ids]
    return await get_student(obj.id)


async def update_student(student: Student, id_student: int) -> Student:
    student_obj = PStudentBase(**student.dict(exclude_unset=True))
    await Student.filter(id=id_student).update(**student_obj.dict(exclude_unset=True))
    obj = await get_student(id_student)
    await obj.courses_list.clear()
    [await obj.courses_list.add(await courses.get_course(id)) for id in student.courses_ids]
    return await Student.get(id=id_student)


async def delete_student(id_student: int) -> dict[str, str]:
    await Student.filter(id=id_student).delete()
    return {"INFO": "Student deleted"}

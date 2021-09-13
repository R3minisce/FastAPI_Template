from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.tortoise import paginate

from schemas.course import PCourseBase
from database.models.manytomany import Course


async def get_course(id_course: int) -> Course:
    obj = await Course.get(id=id_course).prefetch_related()
    obj.students = await obj.students()
    return obj


async def get_courses() -> AbstractPage:
    return await paginate(Course.all())


async def create_course(course: PCourseBase) -> Course:
    return await Course.create(**course.dict(exclude_unset=True))


async def update_course(course: PCourseBase, id_course: int) -> Course:
    await Course.filter(id=id_course).update(**course.dict(exclude_unset=True))
    return await Course.get(id=id_course)


async def delete_course(id_course: int) -> dict[str, str]:
    await Course.filter(id=id_course).delete()
    return {"INFO": "Course deleted"}

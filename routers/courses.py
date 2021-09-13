from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination import Page

from schemas.course import PCourseBase, PCourseDB
from database.models.manytomany import Course
from schemas.student import PCourseStudents
from database.controllers import courses


router = APIRouter(prefix="/course", tags=["courses"])


async def verify_course(id: int) -> Course:
    obj = await courses.get_course(id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return obj


@router.get("/", response_model=Page[PCourseBase])
async def get_courses() -> AbstractPage:
    return await courses.get_courses()


@router.get("/{id}", response_model=PCourseStudents)
async def get_course(id: int) -> Course:
    return await verify_course(id)


@router.post("/", response_model=PCourseDB, status_code=status.HTTP_201_CREATED)
async def create_course(course: PCourseBase) -> Course:
    return await courses.create_course(course)


@router.put("/{id}", response_model=PCourseDB, status_code=status.HTTP_200_OK)
async def update_course(course: PCourseBase, id: int) -> Course:
    if await verify_course(id):
        return await courses.update_course(course, id)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_course(id: int) -> dict[str, str]:
    if await verify_course(id):
        return await courses.delete_course(id)

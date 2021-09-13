from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination import Page

from schemas.student import PStudentCourses, PStudentDB, PStudentCoursesIDs
from database.models.manytomany import Student
from database.controllers import students


router = APIRouter(prefix="/student", tags=["students"])


async def verify_student(id: int) -> Student:
    obj = await students.get_student(id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return obj


@router.get("/", response_model=Page[PStudentDB])
async def get_students() -> AbstractPage:
    return await students.get_students()


@router.get("/{id}", response_model=PStudentCourses)
async def get_student(id: int) -> Student:
    return await verify_student(id)


@router.post("/", response_model=PStudentCourses, status_code=status.HTTP_201_CREATED)
async def create_student(student: PStudentCoursesIDs) -> Student:
    return await students.create_student(student)


@router.put("/{id}", response_model=PStudentDB, status_code=status.HTTP_200_OK)
async def update_student(student: PStudentCoursesIDs, id: int) -> Student:
    if await verify_student(id):
        return await students.update_student(student, id)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_student(id: int) -> dict[str, str]:
    if await verify_student(id):
        return await students.delete_student(id)

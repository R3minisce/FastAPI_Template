from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination import Page

from schemas.child import PChildBase, PChildDB
from database.models.onetomany import Child
from database.controllers import children


router = APIRouter(prefix="/child", tags=["children"])


async def verify_child(id: int) -> Child:
    obj = await children.get_child(id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return obj


@router.get("/", response_model=Page[PChildDB])
async def get_children() -> AbstractPage:
    return await children.get_children()


@router.get("/{id}", response_model=PChildDB)
async def get_child(id: int) -> Child:
    return await verify_child(id)


@router.post("/", response_model=PChildDB, status_code=status.HTTP_201_CREATED)
async def create_child(child: PChildBase) -> Child:
    return await children.create_child(child)


@router.put("/{id}", response_model=PChildDB, status_code=status.HTTP_200_OK)
async def update_child(child: PChildBase, id: int) -> Child:
    if await verify_child(id):
        return await children.update_child(child, id)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_child(id: int) -> dict[str, str]:
    if await verify_child(id):
        return await children.delete_child(id)

from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination import Page

from schemas.parent import PParentBase, PParentDB, PParentChildren
from database.models.onetomany import Parent
from database.controllers import parents


router = APIRouter(prefix="/parent", tags=["parents"])


async def verify_parent(id: int) -> Parent:
    obj = await parents.get_parent(id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return obj


@router.get("/", response_model=Page[PParentDB])
async def get_parents() -> AbstractPage:
    return await parents.get_parents()


@router.get("/{id}", response_model=PParentChildren)
async def get_parent(id: int) -> Parent:
    return await verify_parent(id)


@router.post("/", response_model=PParentDB, status_code=status.HTTP_201_CREATED)
async def create_parent(parent: PParentBase) -> Parent:
    return await parents.create_parent(parent)


@router.put("/{id}", response_model=PParentDB, status_code=status.HTTP_200_OK)
async def update_parent(parent: PParentBase, id: int) -> Parent:
    if await verify_parent(id):
        return await parents.update_parent(parent, id)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_parent(id: int) -> dict[str, str]:
    if await verify_parent(id):
        return await parents.delete_parent(id)

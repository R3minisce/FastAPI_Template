from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.tortoise import paginate

from schemas.parent import PParentBase
from database.models.onetomany import Parent


async def get_parent(id_parent: int) -> Parent:
    obj = await Parent.get(id=id_parent).prefetch_related()
    obj.children_count = await obj.children_count()
    obj.children = await obj.children()
    return obj


async def get_parents() -> AbstractPage:
    return await paginate(Parent.all().prefetch_related())


async def create_parent(parent: PParentBase) -> Parent:
    return await Parent.create(**parent.dict(exclude_unset=True))


async def update_parent(parent: PParentBase, id_parent: int) -> Parent:
    await Parent.filter(id=id_parent).update(**parent.dict(exclude_unset=True))
    return await get_parent(id_parent)


async def delete_parent(id_parent: int) -> dict[str, str]:
    await Parent.filter(id=id_parent).delete()
    return {"INFO": "Parent deleted"}

from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.tortoise import paginate

from schemas.child import PChildBase
from database.models.onetomany import Child


async def get_child(id_child: int) -> Child:
    return await Child.get(id=id_child)


async def get_children() -> AbstractPage:
    return await paginate(Child.all())


async def create_child(child: PChildBase) -> Child:
    return await Child.create(**child.dict(exclude_unset=True))


async def update_child(child: PChildBase, id_child: int) -> Child:
    await Child.filter(id=id_child).update(**child.dict(exclude_unset=True))
    return await Child.get(id=id_child)


async def delete_child(id_child: int) -> dict[str, str]:
    await Child.filter(id=id_child).delete()
    return {"INFO": "Child deleted"}

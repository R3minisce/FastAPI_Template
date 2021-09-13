from tortoise.exceptions import NoValuesFetched
from tortoise.models import Model
from tortoise import fields
from typing import List

from schemas.child import PChildBase


class Child(Model):
    id = fields.IntField(pk=True, generated=True, index=True)
    name = fields.CharField(max_length=25, index=True)
    description = fields.CharField(max_length=50, null=True, index=True)
    parent: fields.ForeignKeyRelation["Parent"] = fields.ForeignKeyField("models.Parent",
                                                                       related_name="children_list",
                                                                       null=True,
                                                                       on_delete=fields.SET_NULL,
                                                                       index=True)

class Parent(Model):
    id = fields.IntField(pk=True, generated=True, index=True)
    name = fields.CharField(max_length=25, index=True)
    description = fields.CharField(max_length=50, null=True, index=True)
    children_list: fields.ReverseRelation[Child]

    async def children_count(self) -> int:
        try:
            return await self.children_list.all().count()
        except NoValuesFetched:
            return -1

    async def children(self) -> List[PChildBase]:
        try:
            return await self.children_list.all()
        except NoValuesFetched:
            return -1

    class PydanticMeta:
        computed = ("children_count", "children_list",)


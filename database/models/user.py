from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True, generated=True, index=True)
    uuid = fields.CharField(max_length=36, unique=True, index=True)
    username = fields.CharField(max_length=25, unique=True, index=True)
    first_name = fields.CharField(max_length=25, index=True)
    last_name = fields.CharField(max_length=25, index=True)
    email = fields.CharField(max_length=25, index=True)
    password = fields.CharField(max_length=255, index=True)
    disabled = fields.BooleanField(index=True, default=False)
    salt = fields.CharField(max_length=255)
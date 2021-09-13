from pydantic import Field, BaseModel

from config.parameters import PASSWORD_POLICY, EMAIL_POLICY
from database.models.user import User


class PUserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, regex="^.+$")
    first_name: str = Field(..., min_length=2, max_length=20, regex="^.+$")
    last_name: str = Field(..., min_length=2, max_length=20, regex="^.+$")
    email: str = Field(..., regex=EMAIL_POLICY)


class PUserDB(PUserBase):
    uuid: str


class PUserPass(PUserBase):
    password: str = Field(..., regex=PASSWORD_POLICY)


class PUserSalt(PUserPass):
    salt: str
    uuid: str


class PUserStatus(PUserBase):
    disabled: bool = Field("False")


class PUserChangePass(BaseModel):
    new_password: str = Field(regex=PASSWORD_POLICY)
    old_password: str = Field(regex=PASSWORD_POLICY)

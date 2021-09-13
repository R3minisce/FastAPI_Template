from fastapi_pagination.ext.tortoise import paginate
from fastapi_pagination.bases import AbstractPage
from fastapi import HTTPException, status
from uuid import uuid4

from schemas.user import PUserPass, User, PUserStatus, PUserSalt, PUserChangePass
from services.dependencies import hash_password, setattrs


async def get_user(uuid: str) -> User:
    return await User.get(uuid=uuid)


async def get_user_by_username(username: str) -> User:
    return await User.get(username=username)


async def get_users() -> AbstractPage:
    return await paginate(User.all())


async def create_user(user: PUserPass) -> User:
    uuid = str(uuid4())
    usernew = PUserSalt(username=user.username, first_name=user.first_name,
                        last_name=user.last_name, email=user.email, salt="", password=user.password, uuid=uuid)
    usernew.password, usernew.salt = hash_password(user.password, None)
    return await User.create(**usernew.dict(exclude_unset=True))


async def update_user(user: PUserStatus, uuid: str) -> User:
    await User.filter(uuid=uuid).update(**user.dict(exclude_unset=True))
    return await get_user(uuid)


async def update_user_password(passwords: PUserChangePass, uuid: str) -> User:
    user_obj = await get_user(uuid)
    old_password, _ = hash_password(passwords.old_password,
                                    user_obj.salt.encode('utf-8'))
    if old_password != user_obj.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    new_password, new_salt = hash_password(passwords.new_password, None)
    setattrs(user_obj, password=new_password, salt=new_salt)
    await user_obj.save()
    return {"INFO": "Password modified"}


async def update_token(uuid: str, jwt: str) -> User:
    user_obj = await get_user(uuid)
    setattrs(user_obj, tmp_jwt=jwt)
    await user_obj.save()
    return await get_user(uuid)


async def delete_user(uuid: str) -> dict[str, str]:
    await User.filter(uuid=uuid).delete()
    return {"INFO": "User deleted"}

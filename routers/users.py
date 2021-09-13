from fastapi import APIRouter, HTTPException, status, Path, Security
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination import Page

from schemas.user import PUserChangePass, PUserDB, PUserPass, PUserStatus, User
from routers.perms import get_current_active_user
from database.controllers import users


router = APIRouter(prefix="/user", tags=["users"])


async def verify_user(uuid: str) -> User:
    obj = await users.get_user(uuid)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return obj


@router.get("/", response_model=Page[PUserDB])
async def get_users() -> AbstractPage:
    return await users.get_users()


@router.get("/uuid/{uuid}", response_model=PUserDB)
async def get_user(uuid: str) -> User:
    return await verify_user(uuid)


@router.get("/username/{username}", response_model=PUserDB)
async def get_user_by_name(username: str = Path(..., max_length=20)) -> User:
    obj = await users.get_user_by_username(username)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await obj


@router.post("/", response_model=PUserDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: PUserPass) -> User:
    return await users.create_user(user)


@router.put("/{uuid}", response_model=PUserDB)
async def update_user(user: PUserStatus, uuid: str,
                      current_user: User = Security(get_current_active_user, scopes=["admin"])) -> User:
    if not await verify_user(uuid):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    return await users.update_user(user, uuid)


@router.put("/ChangePass")
async def change_user_password(passwords: PUserChangePass,
                               current_user: User = Security(get_current_active_user, scopes=["me"])) -> User:
    if await verify_user(current_user.uuid):
        return await users.update_user_password(passwords, current_user.uuid)
        

@router.delete("/{uuid}", status_code=status.HTTP_200_OK)
async def delete_user(uuid: str,
                      current_user: User = Security(get_current_active_user, scopes=["admin"])) -> dict[str, str]:
    if await verify_user(uuid):
        return await users.delete_user(uuid)

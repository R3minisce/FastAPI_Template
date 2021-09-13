import bcrypt

from fastapi import Depends, APIRouter, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes
from datetime import datetime, timedelta
from pydantic import ValidationError
from jose import JWTError, jwt
from typing import Optional

from schemas.token import TokenData, Token
from schemas.user import PUserPass, User
from database.controllers import users
from config.parameters import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM, OAUTH2_SCHEME,
    PRIV_KEY,
    PUB_KEY
)


router = APIRouter(tags=["perms"])


def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


async def get_user(uuid: str) -> User:
    obj = await users.get_user(uuid)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return obj


async def verify_scopes(token_data, security_scopes) -> User:
    user = await get_user(token_data.uuid)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Not enough permissions")
    return user


def extract_token_data(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, PUB_KEY, algorithms=[ALGORITHM])
        uuid: str = payload.get("sub")
        if uuid is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, uuid=uuid)
    except (JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token_data


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(OAUTH2_SCHEME)) -> User:
    token_data = extract_token_data(token)
    return await verify_scopes(token_data, security_scopes)


async def authenticate_user(username: str, password: str) -> User:
    user = await users.get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, PRIV_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get("/token/me/", response_model=PUserPass)
def get_current_active_user(current_user: User = Security(get_current_user, scopes=["me"])) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Inactive user")
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials")
    access_token = create_access_token(
            data={"sub": user.uuid, "scopes": form_data.scopes},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    return {"access_token": access_token, "token_type": "bearer"}

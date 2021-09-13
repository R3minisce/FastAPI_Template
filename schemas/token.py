from typing import Optional, List
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uuid: Optional[str] = None
    scopes: List[str] = []

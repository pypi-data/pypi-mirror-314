from pydantic import BaseModel
from .users import User


class Token(User):
    initData: str


class TokenResponse(BaseModel):
    access_token: str

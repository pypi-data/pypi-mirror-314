import enum
from typing import Optional

from pydantic import BaseModel, model_validator


class UserRoles(enum.Enum):
    user = 'user'
    admin = 'admin'


class User(BaseModel):
    first_name: str
    last_name: Optional[str] = ''
    username: Optional[str] = ''
    tg_id: int
    tg_language: str = ''  # language_code from TG
    language: Optional[str] = None

    @model_validator(mode='after')
    def set_language(cls, model):
        model.language = {
            'en': 'EN',
            'ru': 'RU'
        }.get(model.tg_language, 'EN')
        return model


class UserDB(User):
    invited_by_id: Optional[str] = None
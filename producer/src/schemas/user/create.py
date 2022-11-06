import datetime

from pydantic import BaseModel, validator
from typing import Optional
from src.schemas.newsletter.create import GenreType, get_genre


class User(BaseModel):
    name: str
    email: str
    age: int
    genre: GenreType
    subscription_date: Optional[str]

    @validator('genre', pre=True)
    def set_genre(cls, genre):
        return get_genre(genre)

    @validator('subscription_date', pre=True)
    def set_subscription_date(cls, arg):
        return datetime.datetime.now().isoformat()

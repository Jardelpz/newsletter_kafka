import datetime
import json
import uuid

from pydantic import BaseModel, validator
from enum import Enum
from typing import List, Optional, Union


def get_genre(genre):
    genres = {
        'romance': GenreType.ROMANCE,
        'geek': GenreType.GEEK,
        'news': GenreType.NEWS,
        'sport': GenreType.SPORT
    }

    return genres.get(genre)


class GenreType(Enum):
    ROMANCE = 'romance'
    GEEK = 'geek'
    NEWS = 'news'
    SPORT = 'sport'


class Body(BaseModel):
    subtitle: Optional[str]
    content: str
    image: Optional[str]


class CreateLetter(BaseModel):
    idt: str = None
    title: str
    genre: str
    body: Union[List[Body], str]
    creation_date: str = None

    @validator('idt', pre=True,always=True)
    def set_id(cls, idt):
        return idt or str(uuid.uuid4())

    @validator('creation_date', pre=True, always=True)
    def set_creation_date(cls, creation_date):
        return creation_date or datetime.datetime.now().isoformat()

    @validator('body', pre=True, always=True)
    def convert_body_to_str(cls, body):
        return json.dumps(body)

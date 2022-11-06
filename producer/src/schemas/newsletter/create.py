import datetime
import json
import uuid

from pydantic import BaseModel, validator
from enum import Enum
from typing import List, Optional


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


class CreateLetter(BaseModel):
    id: Optional[str]
    title: str
    genre: GenreType
    body: str
    images: Optional[str]
    creation_date: Optional[str]

    @validator('id', pre=True)
    def set_id(cls, id):
        return str(uuid.uuid4())

    @validator('genre', pre=True)
    def set_genre(cls, genre):
        return get_genre(genre)

    @validator('creation_date', pre=True)
    def set_creation_date(cls, arg):
        return datetime.datetime.now().isoformat()

    @validator('images', pre=True)
    def convert_images_to_str(cls, images):
        return json.dumps(images)

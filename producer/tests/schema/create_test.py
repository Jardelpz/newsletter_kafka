import datetime

import pydantic

from src.schemas.newsletter.create import CreateLetter

payload = {
    'title': 'dsadas',
    'genre': 'romance',
    'body': 'lorem ipsum', #montar um schema de subtitle paragrafo e imagem pra ficar dinamico
    'images': ['sfdasf', 'ffsd'],
    'creation_date': None
}

try:
    a = CreateLetter(**payload)
    print(a)
except pydantic.ValidationError as e:
    print('error in body, status 422', e)

""" FastAPI data model definitions """

from pydantic import BaseModel


class WordleRequest(BaseModel):
    template: str
    guess: str
    answers_left: list
    allowed_left: list
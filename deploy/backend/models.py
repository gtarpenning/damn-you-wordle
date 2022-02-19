""" FastAPI data model definitions """

from pydantic import BaseModel


class WordleRequest(BaseModel):
    id: str
    template: str
    guess: str
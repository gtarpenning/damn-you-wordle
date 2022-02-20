""" FastAPI data model definitions """

from pydantic import BaseModel


class WordleRequest(BaseModel):
    id: str
    sessionID: str
    template: str
    guess: str
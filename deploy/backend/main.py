import uuid

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

import numpy as np
import logging

from models import WordleRequest
import handler


app = FastAPI()


@app.get("/")
def read_root():
    """ Root endpoint, TODO: display basic info (readme?) """
    return {"message": "Wordle Assistant API"}


@app.post("/getword/")
async def advance_wordle_word(req: WordleRequest):
    logging.info(f"Recieved wordle request: [{req.id}: ({req.guess}, {req.template})]")
    return handler.wordle_request(req) or "Endpoint in progress"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)

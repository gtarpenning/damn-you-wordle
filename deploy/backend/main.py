import uuid
import numpy as np
import logging
import json

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from models import WordleRequest
import handler


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Frontend Dev
    "http://localhost:8080",
    "https://damn-you-wordle-app-mpc7znx0v-gtarpenning.vercel.app/", # Frontend Vercel
<<<<<<< HEAD
=======
    "https://damn-you-wordle-app-gtarpenning.vercel.app/", # Another Frontend
>>>>>>> 04eab6a969ac15de7b550800954b54c1bf7b032f
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """ Root endpoint, TODO: display basic info (readme?) """
    return {"message": "Wordle Assistant API"}


@app.post("/getword/")
async def advance_wordle_word(req: WordleRequest):  # WordleRequest
    logging.info(f"Recieved wordle request: ({req.guess}, {req.template})")
    print(f"Recieved wordle request: ({req.guess}, {req.template})")
    return handler.wordle_request(req)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)

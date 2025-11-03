from dotenv import load_dotenv
from typing import Union
from fastapi import FastAPI
import pathlib
import os

import database
import agent


load_dotenv()
SCRIPT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))


database.initialize(rootPath=SCRIPT_DIR)

app = FastAPI()

@app.post('/task')
async def create_task():
    rentals = database.get_rentals()
    result = await agent.run_extract_task(previousContent=rentals)
    return {"rentals": result}

@app.get('/task/{task_id}')
async def get_task(task_id: int):
    return { "task": {}, "status": 'PENDING'}


@app.get("/rentals")
def get_rentals():
    rentals = database.get_rentals()
    return {rentals}

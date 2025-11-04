from dotenv import load_dotenv
from typing import Union
from fastapi import FastAPI, BackgroundTasks, Response, status
import pathlib
import os

from database import Task, Database
import agent


load_dotenv()
SCRIPT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / '../'


database = Database(rootPath=SCRIPT_DIR)

app = FastAPI()

async def launch_task(task: Task):
    rentals = database.get_all_rentals()
    result = await agent.run_extract_task(previousContent=rentals)
    
    task.rentals = result
    task.status = 'DONE'
    database.update_task(task=task)    



@app.post('/task', status_code=201)
def create_task(backgound_task: BackgroundTasks, response: Response):
    pending = database.get_pending_tasks()
    
    if pending is not None:
        response.status_code = status.HTTP_200_OK
        return {"task": pending.to_object()}
         
    
    task = Task();
    
    print(f"taskid ${task.id}")
    
    database.update_task(task=task)

    backgound_task.add_task(launch_task, task)
    
    return {"task": task}

@app.get('/task/{task_id}')
async def get_task(task_id: str, response: Response):
    try:
        task = database.get_task(task_id)
                
        return { "task": task.to_object() }
    except NameError as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        


@app.get("/rentals")
def get_rentals():
    rentals = database.get_all_rentals()
    return {"rentals": rentals}

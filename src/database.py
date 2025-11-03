import pathlib
import os
import json

databaseFile = ''

class Task:
    """Information about a task"""
    id: str
    status: str
    rentals: list

def initialize(rootPath: pathlib.Path):
    """Initialize the database by creating necessary directories and files"""
    
    output_dir = rootPath / '.output'
    databaseFile =  output_dir / 'database.json'

    (output_dir / 'fs').mkdir(exist_ok=True, parents=True)

    if not os.path.exists(databaseFile):
        with databaseFile.open("w", encoding ="utf-8") as f:
            f.write('{}')

    print(f"{databaseFile} was created")

def __save_database(content: list):
    """Save content in database, replace it entirely"""
    with open(databaseFile, 'w') as f:
        json.dump(content, f)
        

def insert_rentals(path: pathlib.Path, task: dict, taskId: int) -> any:
    """Insert content to database"""
    
    database_content = get_database(path)
    database_content[taskId] = task

    __save_database(database_content)
        

def get_database() -> dict:
    """Retrieve whole database"""
    
    with open(database_content, 'r') as f:
        database_content = json.loads(f.read())

    return database_content

def get_task(id: int) -> dict:
    content = get_database()

    if id in content:
        return content[id]
    
    raise NameError(f'task ${id} was not found in database')
        
import pathlib
import os
import json
import time
from typing import Dict

class Task:
    """Information about a task"""
    id: str
    status: str
    rentals: list
    
    def __init__(self, id=None, status='PENDING', rentals=[]):
        if id is None:
            id=str(int(time.time() * 1000000))
        
        self.id = id
        self.status = status
        self.rentals = rentals
        
    def to_object(self):
        return {"id": self.id, "status": self.status, "rentals": self.rentals}


class Database:
    databaseFile: pathlib.Path

    def __init__(self, rootPath: pathlib.Path):
        """Initialize the database by creating necessary directories and files"""
        
        output_dir = rootPath / '.output'
        databaseFile =  output_dir / 'database.json'

        (output_dir / 'fs').mkdir(exist_ok=True, parents=True)

        if not os.path.exists(databaseFile):
            with databaseFile.open("w", encoding ="utf-8") as f:
                f.write('{}')
            print(f"{databaseFile} was initialized")

        self.databaseFile = databaseFile
        

    def __save_database(self, tasks: Dict[str, Task]):
        """Save content in database, replace it entirely"""
        
        documents = {}
        for id in tasks:
            documents[id] = tasks[id].to_object()
        
        print(documents)
        
        with open(self.databaseFile, 'w') as f:
            json.dump(documents, f)
            
    def get_tasks(self) -> Dict[str, Task]:
        """Retrieve whole database"""

        result = {}
        with open(self.databaseFile, 'r') as f:
            database_content = json.loads(f.read())

        for id in database_content:
            result[id] = Task(id=id, status=database_content[id]['status'], rentals=database_content[id]['rentals'])

        return result

    def update_task(self, task: Task) -> any:
        """Insert content to database"""
        
        tasks = self.get_tasks()
        tasks[task.id] = task
        

        self.__save_database(tasks)


    def get_pending_tasks(self) -> Task | None: 
        tasks = self.get_tasks()
        
        for id in tasks:
            if tasks[id].status == 'PENDING':
                return tasks[id]
            
        return None



    def get_task(self, id: int) -> Task | None:
        tasks = self.get_tasks()

        if id in tasks:
            return tasks[id]
        
        raise NameError(f'task ${id} was not found in database')
            
    def get_all_rentals(self) -> list:
        rentals = []
        tasks = self.get_tasks()
                
        for id in tasks:
            if tasks[id].rentals:
                rentals.extend(tasks[id].rentals)
        
        return rentals

from fastapi import FastAPI, Body
from typing import Union
from app.models.tasks import TaskManager

app = FastAPI()
task_manager = TaskManager()

# -- GET METHODS --

@app.get("/")
def root():
    return {"message": "Run..."}

@app.get("/tasks")
def tasks_list():
    return task_manager.list_tasks()

@app.get("/tasks/find")
def find_get(status: Union[str, None] = str()):
    return task_manager.find_task(status)

# -- POST METHODS --

@app.post("/tasks")
def add_post(description: str = Body(...)):
    return task_manager.add_task(description)

# -- PUT METHODS --

@app.put("/tasks/{item_id}/")
def description_put(item_id: int, description: str = Body(...)):
    return task_manager.description_update(item_id, description)

# -- PATCH METHODS --

@app.patch("/tasks/{item_id}/done")
def mark_done_put(item_id: int):
    return task_manager.mark_done(item_id)

@app.patch("/tasks/{item_id}/in-progress")
def mark_progress_put(item_id: int):
    return task_manager.mark_progress(item_id)

# -- DELETE METHODS --

@app.delete("/tasks/{item_id}/")
def delete_method(item_id: int):
    return task_manager.delete_task(item_id)

from fastapi import FastAPI, HTTPException, Body
from typing import Union
from datetime import datetime

import json

class TaskManager:
    def __init__(self):
        self.task = dict()
        self.ids = int()
        self.load_tasks()

    def load_tasks(self):
        try:
            with open("tasks.json", encoding="UTF-8", mode="r") as file:
                self.task = json.load(file)

                if self.task:
                    self.ids = max([int(i) for i in self.task.keys()]) + 1

        except FileNotFoundError:
            self.task = dict()
            self.ids = 1

    def save_tasks(self):
        with open("tasks.json", encoding="UTF-8", mode="w") as file:
            json.dump(self.task, file, indent=4)

    def add_task(self, description: str):
        if not description:
            raise HTTPException(status_code=400, detail="Input cannot be empty")

        self.task.update({str(self.ids): {
            "status": "todo",
            "description": description,
            "date-create": datetime.now().isoformat(),
            "date-update": datetime.now().isoformat()}})

        self.save_tasks()
        self.ids += 1
        return self.task[str(self.ids - 1)]

    def description_update(self, item_id, message):
        if not message:
            raise HTTPException(status_code=400, detail="Input cannot be empty")

        if str(item_id) in self.task.keys():
            self.task[str(item_id)].update({
                "description": str(message),
                "date-update": datetime.now().isoformat()})

            self.save_tasks()
            return self.task[str(item_id)]

        else:
            raise HTTPException(status_code=404, detail="Item not found")

    def delete_task(self, item_id):
        if str(item_id) in self.task.keys():
            del self.task[str(item_id)]
            self.save_tasks()

            return {"Message": f"Item {item_id} delete!"}

        else:
            raise HTTPException(status_code=404, detail="Item not found")

    def mark_done(self, item_id):
        if str(item_id) in self.task.keys():
            self.task[str(item_id)].update({
                "status": "done",
                "date-update": str(datetime.now())})

            self.save_tasks()
            return self.task[str(item_id)]

        else:
            raise HTTPException(status_code=404, detail="Item not found")

    def mark_progress(self, item_id):
        if str(item_id) in self.task.keys():
            self.task[str(item_id)].update({
                "status": "in-progress",
                "date-update": str(datetime.now())})
            
            self.save_tasks()
            return self.task[str(item_id)]

        else:
            raise HTTPException(status_code=404, detail="Item not found")

    def list_tasks(self):
        return self.task

    def find_task(self, item_status):
        if not item_status.strip():
            raise HTTPException(status_code=400, detail="Input cannot be empty")

        else:
            if item_status not in ["todo", "done", "in-progress"]:
                raise HTTPException(status_code=400, detail="Valid inputs: todo / done / in-progress")

            else:
                task_find = dict()
                for task_id, task_info in self.task.items():
                    if task_info["status"] == item_status:
                        task_find.update({task_id: task_info})

                return task_find

app = FastAPI()
task_manager = TaskManager()

# -- GET METHODS --

@app.get("/")
def root():
    return {"message": "Run..."}

@app.get("/tasks")
def list():
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

if __name__ == "__main__":
    from uvicorn import run
    run(app, host="127.0.0.1", port=8080)

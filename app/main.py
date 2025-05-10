from fastapi import FastAPI
from typing import Union

import json
import datetime

class TaskManager:
    def __init__(self):
        self.task = dict()
        self.ids = int()
        self.json_atualizer()

    def json_atualizer(self):
        try:
            with open("tasks.json", encoding="UTF-8", mode="r") as file:
                self.task = json.load(file)

        except FileNotFoundError:
            self.task = dict()
            self.ids = int()

    def json_converter(self):
        with open("tasks.json", encoding="UTF-8", mode="w") as file:
            json.dump(self.task, file, indent=4)

    def add_task(self):
        while str(self.ids) in self.task:
            self.ids += 1

        self.task.update({str(self.ids): {
            "status": "todo",
            "description": str(),
            "date-create": str(datetime.datetime.now()),
            "date-update": str(datetime.datetime.now())
            }})

        self.json_converter()
        return self.task[str(self.ids)]

    def list_tasks(self):
        return self.task

    def description_update(self, item_id, message):
        if str(item_id) in self.task.keys():
            self.task[str(item_id)].update({
                "description": str(message),
                "date-update": str(datetime.datetime.now)})

            self.json_converter()
            return self.task[str(item_id)]

        else:
            return{"Message": f"Item {item_id} not found"}

    def delete_task(self, item_id):
        if str(item_id) in self.task.keys():
            del self.task[str(item_id)]
            self.json_converter()

            return {"Message": f"Item {item_id} delete!"}

        else:
            return {"Message": f"Item {item_id} not found!"}

    def mark_done(self, item_id):
        if str(item_id) in self.task.keys():
            self.task[str(item_id)].update({
                "status": "done",
                "date-update": str(datetime.datetime.now())})

            self.json_converter()
            return self.task[str(item_id)]

        else:
            return {"Message": f"Item {item_id} not found"}

    def mark_progress(self, item_id):
        if str(item_id) in self.task.keys():
            self.task[str(item_id)].update({
                "status": "in-progress",
                "date-update": str(datetime.datetime.now())})
            
            self.json_converter()
            return self.task[str(item_id)]
        else:
            return {"Message": f"Item {item_id} not fount"}

    def find_task(self, item_status):
        if item_status not in ["todo", "done", "in-progress"]:
            return {"Message": "Valid inputs: todo / done / in-progress"}

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
    return "Run..."

@app.get("/tasks")
def list():
    return task_manager.list_tasks()

@app.get("/tasks/find")
def find_get(status: Union[str, None] = str()):
    return task_manager.find_task(status)

# -- POST METHODS --

@app.post("/tasks")
def add_post():
    return task_manager.add_task()

# -- PUT METHODS --

@app.put("/tasks/{item_id}/")
def description_put(item_id: int, q: Union[str, None] = str()):
    return task_manager.description_update(item_id, q)

# -- PATCH METHODS --

@app.patch("/tasks/{item_id}/done")
def mark_done_put(item_id: int):
    return task_manager.mark_done(item_id)

@app.put("/tasks/{item_id}/in-progress")
def mark_progress_put(item_id: int):
    return task_manager.mark_progress(item_id)

# -- DELETE METHODS --

@app.delete("/tasks/{item_id}/")
def delete_method(item_id: int):
    return task_manager.delete_task(item_id)

if __name__ == "__main__":
    from uvicorn import run
    run(app, host="127.0.0.1", port=8080)

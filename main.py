from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    task: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[str] = None
    length: Optional[int] = None

app = FastAPI()

@app.get("/")
def index():
    return{"launch":"successful"}

todo_list = {
    1: {
        "task": "create todo list 1",
        "description": "to-do list uing FastAPI and CRUD structure",
        "deadline": "1/3/24",
        "length": 1
    },

    2: {
        "task": "create todo list 2",
        "description": "to-do list uing FastAPI and CRUD structure",
        "deadline": "1/3/24",
        "length": 1
    }
}

@app.get("/get-item/{item_number}")
def get_item( item_number: Optional[int] = Path(..., description="Item number")):
    if item_number not in todo_list:
        return{"Error": "ID does not exist"}
    return todo_list[item_number]

@app.get("/search-task")
def search_task(task: str = Query(..., description="Task to search")):
    match = []
    for item_number in todo_list.values():
        if task in item_number["task"]:
            match.append(item_number)
    if not match:
        return{"Error": "Task not found"}
    return match

@app.post("/create-task/{item_number}")
def create_task(item: Item, item_number: int = Path(..., description="New task number")):
    if item_number in todo_list:
        return {"Error": "item number already exist"}
    todo_list[item_number] = item.dict()
    return todo_list[item_number]

@app.put("/update-task/{item_number}")
def update_task(item: Item, item_number: int):
    if item_number not in todo_list:
        return {"Error": "item number does not exist"}
    for key, value in item.__dict__.items():
        if key in todo_list[item_number] and value is not None:
            todo_list[item_number][key] = value
    return todo_list[item_number]

@app.delete("/delete-task/{item_number}")
def delete_task(item_number:int):
    if item_number not in todo_list:
        return {"Error": "item number does not exist"}
    del todo_list[item_number]
    return{"Message": f"item {item_number} deleted"}
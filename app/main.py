from fastapi import FastAPI, HTTPException
from typing import List

from app.database.models import Todo
from app.crud import (
    get_all_todos, create_task, get_single_task, 
    update_task, delete_task, insert_multiple_tasks
)

app = FastAPI(title="Todo API using FastAPI and MongoDB")


@app.get("/todos")
async def list_todos():
    return get_all_todos()


@app.post("/todos")
async def add_todo(new_task: Todo):
    try:
        return create_task(new_task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")


@app.get("/todos/{task_id}")
async def get_todo(task_id: str):
    todo = get_single_task(task_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Task does not exist")
    return todo


@app.put("/todos/{task_id}")
async def update_todo(task_id: str, updated_task: Todo):
    try:
        updated = update_task(task_id, updated_task)
        if not updated:
            raise HTTPException(status_code=404, detail="Task does not exist")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")


@app.delete("/todos/{task_id}")
async def remove_todo(task_id: str):
    try:
        deleted_count = delete_task(task_id)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task does not exist")
        return {"status_code": 200, "message": "Task Deleted Successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")


@app.post("/todos/bulk")
async def add_multiple_todos(tasks: List[Todo]):
    try:
        data = [t.model_dump() for t in tasks]
        return insert_multiple_tasks(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")



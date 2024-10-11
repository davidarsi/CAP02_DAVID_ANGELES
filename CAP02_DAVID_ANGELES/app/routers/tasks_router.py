"""
Provides an API router for managing tasks.

The `tasks_router` API router defines the following endpoints:

- `POST /`: Creates a new task.
- `GET /{task_id}`: Retrieves a task by its ID.
- `GET /`: Retrieves a list of all tasks.
- `PUT /{task_id}`: Updates a task by its ID.
- `DELETE /{task_id}`: Deletes a task by its ID.
- `DELETE /`: Deletes all tasks.
"""
from fastapi import APIRouter, HTTPException
from models import Task, UpdateTaskModel, TaskList
from db import db

tasks_router = APIRouter()


@tasks_router.post("/", response_model=Task)
async def create_task(task: Task):
    return db.add_task(task)


"""
Retrieves a task by its ID.

Args:
    task_id (int): The ID of the task to retrieve.

Returns:
    Task: The task with the specified ID.

Raises:
    HTTPException: If the task with the specified ID is not found.
"""
@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@tasks_router.get("/", response_model=TaskList)
async def get_tasks(skip: int = 0, limit: int = 10):
    tasks = db.get_tasks(skip=skip, limit=limit)
    total = db.get_total_tasks()
    return TaskList(tasks=tasks, total=total, skip=skip, limit=limit)


@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int):
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}

#Agregar un endpoint que me permita eliminar todos los registros de la base de datos
@tasks_router.delete("/")
async def delete_all_tasks():
    db.delete_all_tasks()
    return {"message": "All tasks deleted successfully"}
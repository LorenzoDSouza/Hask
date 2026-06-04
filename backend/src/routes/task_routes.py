from fastapi import APIRouter, Depends, HTTPException
from models import Task
from dependencies import get_session
from sqlalchemy.orm import Session
from schemas import TaskRequest, UpdateTaskRequest


task_router = APIRouter(prefix="/tasks", tags=["tasks"])

@task_router.get("")
async def tasks():
    """
    This is the route to list all the tasks
    """
    return {"message": "You accessed the tasks"}

@task_router.post("/task")
async def create_task(task_request: TaskRequest, session: Session = Depends(get_session)):
    
    new_task = Task(task_request.title, task_request.user_id, task_request.category, task_request.status)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return {"message": f"Task '{new_task.title}' created succesfully! New task id: {new_task.id}"}

@task_router.put("/task")
async def update_task(task_request: UpdateTaskRequest, session: Session = Depends(get_session)):
    task = session.query(Task).filter(Task.id==task_request.id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Couldn't update task because no task was found with Id {task_request.id}!")

    if task_request.title is not None:
        task.title = task_request.title
    if task_request.status is not None:
        task.status = task_request.status
    if task_request.user_id is not None:
        task.user_id = task_request.user_id
    if task_request.category is not None:
        task.category = task_request.category

    session.commit()
    session.refresh(task)

    return {"message": f"Task '{task.title}' updated succesfully!"}
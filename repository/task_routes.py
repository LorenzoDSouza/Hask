from fastapi import APIRouter, Depends, HTTPException
from models import Task
from dependencies import get_session
from sqlalchemy.orm import Session
from schemas import TaskRequest


task_router = APIRouter(prefix="/tasks", tags=["tasks"])

@task_router.get("/")
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
    return {"Task '{new_task.title}' created succesfully! New task id: {new_task.id}"}

@task_router.get("/tasks/{user_id}/{task_id}")
async def get_user_by_id(user_id: int, task_id: int, session: Session = Depends(get_session)):
    task = session.query(Task).filter(Task.user_id==user_id & Task.id==task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="User not found with id {user_id}!")
    
    return task
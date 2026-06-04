from fastapi import APIRouter, Depends, HTTPException
from models import Task, User
from dependencies import get_session
from sqlalchemy.orm import Session
from schemas import TaskRequest


task_router = APIRouter(prefix="/tasks", tags=["tasks"])

@task_router.post("/", status_code=201)
async def create_task(task_request: TaskRequest, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id == task_request.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User not found with id {task_request.user_id}")
    
    new_task = Task(task_request.title, task_request.user_id, task_request.category, task_request.status)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task

@task_router.get("/{task_id}")
async def get_task_by_id(task_id: int, session: Session = Depends(get_session)):    
    task = session.query(Task).filter(Task.id==task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found with id {task_id}!")
    
    return task

@task_router.delete("/{task_id}")
async def delete_task_by_id(task_id: int,  session: Session = Depends(get_session)):
    task = session.query(Task).filter(Task.id==task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found with id {task_id}!")
    
    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully!"}

@task_router.put("/{task_id}")
async def update_task_by_id(task_request: TaskRequest, task_id: int, session: Session = Depends(get_session)):
    task = session.query(Task).filter(Task.id== task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found with id {task_id}!")
    
    new_user_assigned = session.query(User).filter(User.id==task_request.user_id).first()
    
    if not new_user_assigned:
        raise HTTPException(status_code=404, detail=f"The new user you are trying to assign to the task does not exist: {task_request.user_id}!")

    task.title = task_request.title
    task.user_id = task_request.user_id
    task.category = task_request.category
    task.status = task_request.status

    session.commit()
    session.refresh(task)

    return task

@task_router.get("/")
async def get_tasks(category: str | None = None, session: Session = Depends(get_session)):
    query = session.query(Task)

    if category:
        query = query.filter(Task.category == category)

    return query.all()
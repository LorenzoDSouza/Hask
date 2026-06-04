from fastapi import APIRouter, Depends, HTTPException
from models import Task, User
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
    return {f"Task '{new_task.title}' created succesfully! New task id: {new_task.id}"}

@task_router.get("/tasks/{user_id}/{task_id}")
async def get_task_by_id(user_id: int, task_id: int, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User not found with id {user_id}!")
    
    task = session.query(Task).filter(Task.user_id==user_id & Task.id==task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found with id {task_id}!")
    
    return task

@task_router.delete("/{user_id}/{task_id}")
async def delete_task_by_id(user_id: int, task_id: int,  session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User not found with id {user_id}!")

    task = session.query(Task).filter(Task.user_id==user_id & Task.id==task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found with id {task_id}!")
    
    session.delete(task)
    session.commit()

    return {"message": "User deleted successfully!"}

@task_router.put("/{user_id}/{task_id}")
async def update_task_by_id(task_request: TaskRequest, user_id: int, task_id: int, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User not found with id {user_id}!")
    
    task = session.query(Task).filter(Task.user_id==user_id & Task.task_id== task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found with id {task_id}!")
    
    new_user_assigned = session.query(User).filter(User.id==task_request.user_id).first()
    
    if not new_user_assigned:
        raise HTTPException(status_code=404, detail=f"The new user you are trying to assign to the task does not exist: {user_id}!")

    task.title = task_request.title
    task.user_id = task_request.user_id
    task.category = task_request.category
    task.status = task_request.status

    session.commit()
    session.refresh(task)

    return task
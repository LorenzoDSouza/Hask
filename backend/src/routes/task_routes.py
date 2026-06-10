from fastapi import APIRouter, Depends, HTTPException
from src.utils.calendar_service import CalendarService
from src.utils.mail_service import notify_task_created, notify_task_updated, notify_task_deleted
from models import Task, User
from dependencies import get_current_user, get_session
from sqlalchemy.orm import Session
from schemas import TaskRequest, UpdateTaskRequest
from services.task_service import TaskService

task_router = APIRouter(prefix="/tasks", tags=["tasks"])

calendar_service = CalendarService()

@task_router.get("/")
async def tasks(session: Session = Depends(get_session)):
    """
    This is the route to list all the tasks
    """
    return session.query(Task).all()

@task_router.post("/", status_code=201)
async def create_task(task_request: TaskRequest, session: Session = Depends(get_session), user = Depends(get_current_user)):
    new_task = Task(task_request.title, task_request.user_id, task_request.category, task_request.start_date_time, task_request.end_date_time, task_request.status)

    task_user = session.query(User).filter(User.id == task_request.user_id).first()
    if not task_user:
        raise HTTPException(status_code=404, detail=f"User not found with id {task_request.user_id}")

    if new_task.start_date_time and new_task.end_date_time and task_user.calendar_connected:
        calendar_service.create_event(task_user, new_task.title, new_task.category, new_task.start_date_time, new_task.end_date_time)

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    notify_task_created(task_user.name, task_user.email, new_task.title, new_task.category)

    return {"message": f"Task '{new_task.title}' created succesfully! New task id: {new_task.id}"}

@task_router.get("/{task_id}")
async def get_task_by_id(task_id: int, session: Session = Depends(get_session)):    
    task_service = TaskService(session)

    return task_service.get_task_by_id(task_id)

@task_router.delete("/{task_id}")
async def delete_task_by_id(task_id: int, session: Session = Depends(get_session)):
    task = session.query(Task).filter(Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found with id {task_id}!")

    task_user = session.query(User).filter(User.id == task.user_id).first()
    task_title = task.title
    session.delete(task)
    session.commit()

    if task_user:
        notify_task_deleted(task_user.name, task_user.email, task_title)

    return {"message": "Task deleted successfully!"}

@task_router.put("/{task_id}")
async def update_task(task_id: int, task_request: UpdateTaskRequest, session: Session = Depends(get_session)):
    task = session.query(Task).filter(Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Couldn't update task because no task was found with Id {task_request.id}!")

    old_status = task.status

    if task_request.title is not None:
        task.title = task_request.title
    if task_request.status is not None:
        task.status = task_request.status
    if task_request.user_id is not None:
        task_user = session.query(User).filter(User.id == task_request.user_id).first()
        if not task_user:
            raise HTTPException(status_code=404, detail=f"User not found with id {task_request.user_id}")
        task.user_id = task_request.user_id
        notify_task_updated(task_user.name, task_user.email, task.title, old_status, task.status, reassigned=True)
    if task_request.category is not None:
        task.category = task_request.category

    session.commit()
    session.refresh(task)

    return task
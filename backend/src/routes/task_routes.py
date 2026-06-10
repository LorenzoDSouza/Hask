from fastapi import APIRouter, Depends
from dependencies import get_current_user, get_session
from sqlalchemy.orm import Session
from schemas import TaskRequest, UpdateTaskRequest
from src.services.task_service import TaskService

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.get("/")
async def tasks(session: Session = Depends(get_session)):
    """List all the tasks."""
    return TaskService(session).list_tasks()


@task_router.post("/", status_code=201)
async def create_task(
    task_request: TaskRequest,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    return TaskService(session).create_task(task_request)


@task_router.get("/{task_id}")
async def get_task_by_id(task_id: int, session: Session = Depends(get_session)):
    return TaskService(session).get_task_by_id(task_id)


@task_router.delete("/{task_id}")
async def delete_task_by_id(task_id: int, session: Session = Depends(get_session)):
    return TaskService(session).delete_task(task_id)


@task_router.put("/{task_id}")
async def update_task(
    task_id: int,
    task_request: UpdateTaskRequest,
    session: Session = Depends(get_session),
):
    return TaskService(session).update_task(task_id, task_request)

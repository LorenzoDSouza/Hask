from fastapi import HTTPException
from models import Task
from src.repositories.task_repository import TaskRepository
from src.repositories.user_repository import UserRepository
from src.services.calendar_service import CalendarService
from src.services import mail_service as default_mailer


class TaskService:
    def __init__(
        self,
        session=None,
        *,
        task_repo=None,
        user_repo=None,
        calendar_service=None,
        mailer=None,
    ):
        self.task_repo = task_repo or TaskRepository(session)
        self.user_repo = user_repo or UserRepository(session)
        self.calendar_service = (
            calendar_service if calendar_service is not None else CalendarService()
        )
        self.mailer = mailer if mailer is not None else default_mailer

    def list_tasks(self):
        return self.task_repo.list_all()

    def get_task_by_id(self, task_id: int):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task not found with id {task_id}")
        return task

    def create_task(self, data) -> dict:
        task_user = self.user_repo.get_by_id(data.user_id)
        if not task_user:
            raise HTTPException(status_code=404, detail=f"User not found with id {data.user_id}")

        new_task = Task(
            data.title,
            data.user_id,
            data.category,
            data.start_date_time,
            data.end_date_time,
            data.status,
        )

        # Cria o evento no Google Calendar antes de persistir (mesma ordem do codigo original).
        if new_task.start_date_time and new_task.end_date_time and task_user.calendar_connected:
            self.calendar_service.create_event(
                task_user,
                new_task.title,
                new_task.category,
                new_task.start_date_time,
                new_task.end_date_time,
            )

        self.task_repo.add(new_task)

        self.mailer.notify_task_created(
            task_user.name, task_user.email, new_task.title, new_task.category
        )

        return {
            "message": f"Task '{new_task.title}' created succesfully! New task id: {new_task.id}"
        }

    def update_task(self, task_id: int, data) -> Task:
        task = self.get_task_by_id(task_id)
        old_status = task.status

        if data.title is not None:
            task.title = data.title
        if data.status is not None:
            task.status = data.status
        if data.user_id is not None:
            task_user = self.user_repo.get_by_id(data.user_id)
            if not task_user:
                raise HTTPException(status_code=404, detail=f"User not found with id {data.user_id}")
            task.user_id = data.user_id
            self.mailer.notify_task_updated(
                task_user.name, task_user.email, task.title, old_status, task.status, reassigned=True
            )
        if data.category is not None:
            task.category = data.category

        return self.task_repo.save(task)

    def delete_task(self, task_id: int) -> dict:
        task = self.get_task_by_id(task_id)
        task_user = self.user_repo.get_by_id(task.user_id)
        task_title = task.title

        self.task_repo.delete(task)

        if task_user:
            self.mailer.notify_task_deleted(task_user.name, task_user.email, task_title)

        return {"message": "Task deleted successfully!"}

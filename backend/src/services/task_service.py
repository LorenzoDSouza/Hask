from repositories.task_repository import TaskRepository
from fastapi import HTTPException
class TaskService:

    def __init__(self, session):
        self.repository = TaskRepository(session)

    def get_task_by_id(self, task_id: int):
        task = self.repository.get_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail=f"Task not found with id {task_id}")
        
        return task
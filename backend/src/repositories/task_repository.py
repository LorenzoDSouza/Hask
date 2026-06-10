from models import Task


class TaskRepository:
    """Acesso a dados da entidade Task. Sem regra de negocio."""

    def __init__(self, session):
        self.session = session

    def get_by_id(self, task_id: int):
        return self.session.query(Task).filter(Task.id == task_id).first()

    def list_all(self):
        return self.session.query(Task).all()

    def add(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def save(self, task: Task) -> Task:
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()

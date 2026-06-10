from models import Task

class TaskRepository:

    def __init__(self, session):
        self.session = session

    def get_by_id(self, task_id: int):
        return(self.session.query(Task).filter(Task.id==task_id).first())
    
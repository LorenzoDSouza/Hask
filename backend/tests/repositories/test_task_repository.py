from models import User, Task, TaskStatus
from src.repositories.task_repository import TaskRepository
from src.repositories.user_repository import UserRepository


def _make_user(db_session):
    return UserRepository(db_session).add(User("A", "a@a.com", "hash"))


def test_add_and_get_by_id(db_session):
    user = _make_user(db_session)
    repo = TaskRepository(db_session)
    task = repo.add(Task("T1", user.id, "cat", None, None, TaskStatus.TODO))
    assert task.id is not None
    assert repo.get_by_id(task.id).title == "T1"


def test_list_all(db_session):
    user = _make_user(db_session)
    repo = TaskRepository(db_session)
    repo.add(Task("T1", user.id, "cat", None, None, TaskStatus.TODO))
    repo.add(Task("T2", user.id, "cat", None, None, TaskStatus.IN_PROGRESS))
    assert len(repo.list_all()) == 2


def test_delete(db_session):
    user = _make_user(db_session)
    repo = TaskRepository(db_session)
    task = repo.add(Task("T1", user.id, "cat", None, None, TaskStatus.TODO))
    repo.delete(task)
    assert repo.get_by_id(task.id) is None

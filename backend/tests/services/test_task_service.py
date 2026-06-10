from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException
from src.services.task_service import TaskService
from models import TaskStatus


def make_data(user_id=1, start=None, end=None, status=TaskStatus.TODO, title="T", category="c"):
    return SimpleNamespace(
        title=title,
        user_id=user_id,
        category=category,
        status=status,
        start_date_time=start,
        end_date_time=end,
    )


def build_service(*, user=None, task=None):
    user_repo = MagicMock()
    user_repo.get_by_id.return_value = user
    task_repo = MagicMock()
    task_repo.get_by_id.return_value = task
    task_repo.save.side_effect = lambda t: t
    calendar = MagicMock()
    mailer = MagicMock()
    svc = TaskService(
        task_repo=task_repo, user_repo=user_repo, calendar_service=calendar, mailer=mailer
    )
    return svc, task_repo, user_repo, calendar, mailer


def test_create_task_user_not_found_404():
    svc, *_ = build_service(user=None)
    with pytest.raises(HTTPException) as exc:
        svc.create_task(make_data())
    assert exc.value.status_code == 404


def test_create_task_creates_event_when_connected():
    user = SimpleNamespace(id=1, name="A", email="a@a.com", calendar_connected=True)
    svc, task_repo, _, calendar, mailer = build_service(user=user)
    svc.create_task(make_data(start="2026-06-10T10:00:00", end="2026-06-10T11:00:00"))
    calendar.create_event.assert_called_once()
    mailer.notify_task_created.assert_called_once()
    task_repo.add.assert_called_once()


def test_create_task_no_event_when_not_connected():
    user = SimpleNamespace(id=1, name="A", email="a@a.com", calendar_connected=False)
    svc, _, _, calendar, mailer = build_service(user=user)
    svc.create_task(make_data(start="2026-06-10T10:00:00", end="2026-06-10T11:00:00"))
    calendar.create_event.assert_not_called()
    mailer.notify_task_created.assert_called_once()


def test_create_task_no_event_without_dates():
    user = SimpleNamespace(id=1, name="A", email="a@a.com", calendar_connected=True)
    svc, _, _, calendar, _ = build_service(user=user)
    svc.create_task(make_data())
    calendar.create_event.assert_not_called()


def test_get_task_not_found_404():
    svc, *_ = build_service(task=None)
    with pytest.raises(HTTPException) as exc:
        svc.get_task_by_id(5)
    assert exc.value.status_code == 404


def test_delete_task_notifies():
    task = SimpleNamespace(id=3, title="T", user_id=1)
    user = SimpleNamespace(name="A", email="a@a.com")
    svc, task_repo, _, _, mailer = build_service(user=user, task=task)
    result = svc.delete_task(3)
    task_repo.delete.assert_called_once_with(task)
    mailer.notify_task_deleted.assert_called_once()
    assert "deleted" in result["message"].lower()


def test_update_task_reassign_notifies():
    task = SimpleNamespace(id=3, title="T", user_id=1, status=TaskStatus.TODO)
    new_user = SimpleNamespace(name="B", email="b@b.com")
    svc, _, _, _, mailer = build_service(user=new_user, task=task)
    data = SimpleNamespace(
        title=None, status=None, user_id=2, category=None, start_date_time=None, end_date_time=None
    )
    svc.update_task(3, data)
    mailer.notify_task_updated.assert_called_once()

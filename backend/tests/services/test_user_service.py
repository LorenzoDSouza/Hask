from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException
from src.services.user_service import UserService


def test_create_user_success():
    repo = MagicMock()
    repo.email_exists.return_value = False
    repo.add.side_effect = lambda u: u
    user = UserService(user_repo=repo).create_user("A", "a@a.com", "pw")
    assert user.email == "a@a.com"
    repo.add.assert_called_once()


def test_create_user_duplicate_email_409():
    repo = MagicMock()
    repo.email_exists.return_value = True
    with pytest.raises(HTTPException) as exc:
        UserService(user_repo=repo).create_user("A", "a@a.com", "pw")
    assert exc.value.status_code == 409


def test_get_user_not_found_404():
    repo = MagicMock()
    repo.get_by_id.return_value = None
    with pytest.raises(HTTPException) as exc:
        UserService(user_repo=repo).get_user(99)
    assert exc.value.status_code == 404


def test_update_user_email_conflict_409():
    repo = MagicMock()
    repo.get_by_id.return_value = MagicMock()
    repo.email_exists.return_value = True
    with pytest.raises(HTTPException) as exc:
        UserService(user_repo=repo).update_user(1, "A", "dup@a.com", "pw")
    assert exc.value.status_code == 409


def test_delete_user_not_found_404():
    repo = MagicMock()
    repo.get_by_id.return_value = None
    with pytest.raises(HTTPException) as exc:
        UserService(user_repo=repo).delete_user(1)
    assert exc.value.status_code == 404

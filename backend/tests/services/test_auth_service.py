from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException
from src.services.auth_service import AuthService
from security import hash_password


def build_user(password="secret"):
    return SimpleNamespace(id=1, email="a@a.com", password=hash_password(password))


def test_authenticate_success():
    repo = MagicMock()
    repo.get_by_email.return_value = build_user("secret")
    assert AuthService(user_repo=repo).authenticate("a@a.com", "secret") is not None


def test_authenticate_wrong_password():
    repo = MagicMock()
    repo.get_by_email.return_value = build_user("secret")
    assert AuthService(user_repo=repo).authenticate("a@a.com", "wrong") is None


def test_authenticate_user_not_found():
    repo = MagicMock()
    repo.get_by_email.return_value = None
    assert AuthService(user_repo=repo).authenticate("x@x.com", "secret") is None


def test_login_returns_token():
    repo = MagicMock()
    repo.get_by_email.return_value = build_user("secret")
    result = AuthService(user_repo=repo).login("a@a.com", "secret")
    assert "access_token" in result
    assert result["token_type"] == "bearer"


def test_login_invalid_raises_401():
    repo = MagicMock()
    repo.get_by_email.return_value = None
    with pytest.raises(HTTPException) as exc:
        AuthService(user_repo=repo).login("x@x.com", "y")
    assert exc.value.status_code == 401

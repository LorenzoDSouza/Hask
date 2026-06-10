from models import User
from src.repositories.user_repository import UserRepository


def make_user(name="A", email="a@a.com", password="hash"):
    return User(name, email, password)


def test_add_and_get_by_id(db_session):
    repo = UserRepository(db_session)
    user = repo.add(make_user())
    assert user.id is not None
    assert repo.get_by_id(user.id).email == "a@a.com"


def test_get_by_email(db_session):
    repo = UserRepository(db_session)
    repo.add(make_user(email="b@b.com"))
    assert repo.get_by_email("b@b.com") is not None
    assert repo.get_by_email("none@none.com") is None


def test_email_exists_with_exclude(db_session):
    repo = UserRepository(db_session)
    user = repo.add(make_user(email="c@c.com"))
    assert repo.email_exists("c@c.com") is True
    assert repo.email_exists("c@c.com", exclude_id=user.id) is False
    assert repo.email_exists("x@x.com") is False


def test_list_all_and_delete(db_session):
    repo = UserRepository(db_session)
    user1 = repo.add(make_user(email="d1@d.com"))
    repo.add(make_user(email="d2@d.com"))
    assert len(repo.list_all()) == 2
    repo.delete(user1)
    assert len(repo.list_all()) == 1

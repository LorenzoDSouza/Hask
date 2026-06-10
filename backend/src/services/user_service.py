from fastapi import HTTPException
from models import User
from src.repositories.user_repository import UserRepository
from security import hash_password


class UserService:
    def __init__(self, session=None, *, user_repo=None):
        self.user_repo = user_repo or UserRepository(session)

    def create_user(self, name: str, email: str, password: str) -> User:
        if self.user_repo.email_exists(email):
            raise HTTPException(status_code=409, detail="Email alredy been used by another user!")
        user = User(name, email, hash_password(password))
        return self.user_repo.add(user)

    def get_user(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User not found with id {user_id}!")
        return user

    def list_users(self):
        return self.user_repo.list_all()

    def update_user(self, user_id: int, name: str, email: str, password: str) -> User:
        user = self.get_user(user_id)

        if self.user_repo.email_exists(email, exclude_id=user_id):
            raise HTTPException(status_code=409, detail=f"Email {email} already in use!")

        user.name = name
        user.email = email
        user.password = hash_password(password)
        return self.user_repo.save(user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.user_repo.delete(user)

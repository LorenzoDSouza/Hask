from fastapi import HTTPException
from src.repositories.user_repository import UserRepository
from security import verify_password, create_access_token


class AuthService:
    def __init__(self, session=None, *, user_repo=None):
        self.user_repo = user_repo or UserRepository(session)

    def authenticate(self, email: str, password: str):
        """Retorna o User se as credenciais batem, senao None."""
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def login(self, email: str, password: str) -> dict:
        user = self.authenticate(email, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials!")
        access_token = create_access_token(user.id)
        return {"access_token": access_token, "token_type": "bearer"}

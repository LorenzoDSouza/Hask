from fastapi import HTTPException
from src.repositories.user_repository import UserRepository
from src.services.calendar_service import CalendarService


class CalendarConnectionService:
    """Orquestra a conexao da conta Google Calendar do usuario."""

    def __init__(self, session=None, *, user_repo=None, calendar_service=None):
        self.user_repo = user_repo or UserRepository(session)
        self.calendar_service = (
            calendar_service if calendar_service is not None else CalendarService()
        )

    def authorization_url(self, state: str) -> str:
        return self.calendar_service.get_authorization_url(state)

    def connect(self, user_id: int, code: str):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        credentials = self.calendar_service.exchange_code_for_tokens(code)
        user.google_refresh_token = credentials["refresh_token"]
        user.calendar_connected = True
        return self.user_repo.save(user)

    def disconnect(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.google_refresh_token = None
        user.calendar_connected = False
        return self.user_repo.save(user)

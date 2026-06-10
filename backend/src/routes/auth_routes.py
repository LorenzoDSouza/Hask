from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dependencies import get_session, get_current_user
from config import FRONTEND_URL
from security import create_access_token, decode_token
from schemas import LoginRequest
from models import User
from src.services.auth_service import AuthService
from src.services.calendar_connection_service import CalendarConnectionService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("")
async def home():
    """Standard authentication route for the API."""
    return {"message": "You accessed the standardt auth route", "authenticated": False}


@auth_router.post("/login")
async def login(login_request: LoginRequest, session: Session = Depends(get_session)):
    return AuthService(session).login(login_request.email, login_request.password)


@auth_router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": f"User {current_user.email} logged out succesfully!"}


@auth_router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """OAuth2 password flow usado pelo botao Authorize do Swagger (username = email)."""
    return AuthService(session).login(form_data.username, form_data.password)


@auth_router.get("/google/authorize")
async def google_authorize(current_user: User = Depends(get_current_user)):
    state = create_access_token(current_user.id)
    return {"authorization_url": CalendarConnectionService().authorization_url(state)}


@auth_router.get("/google/callback")
async def google_callback(code: str, state: str, session: Session = Depends(get_session)):
    """
    Callback chamado pelo Google apos o consentimento. Salva as credenciais e
    redireciona de volta para o frontend.
    """
    try:
        user_id = decode_token(state)
        if user_id is None:
            raise ValueError("invalid state token")
        CalendarConnectionService(session).connect(user_id, code)
    except Exception:
        return RedirectResponse(f"{FRONTEND_URL}/?calendar=error")

    return RedirectResponse(f"{FRONTEND_URL}/?calendar=connected")


@auth_router.delete("/google/disconnect")
async def google_disconnect(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    CalendarConnectionService(session).disconnect(current_user.id)
    return {"message": "Google Calendar disconnected successfully"}

import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from src.services.calendar_service import CalendarService
from models import User
from dependencies import get_session, get_current_user
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserRequest, LoginRequest
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta, timezone

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

auth_router = APIRouter(prefix="/auth", tags=["auth"])

calendar_service = CalendarService()
    
def create_token(user_id):
    expire_date = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dic_info = {"sub": str(user_id), "exp": int(expire_date.timestamp())}

    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def auth_user(email: str, password: str, session: Session):
    user = session.query(User).filter(User.email==email).first()

    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.password):
        return False

    return user

@auth_router.get("")
async def home():
    """
    This is the standardt authentication route for the API
    """
    return {"message": "You accessed the standardt auth route", "authenticated": False}


@auth_router.post("/login")
async def login(login_request: LoginRequest, session: Session = Depends(get_session)):
    user = auth_user(login_request.email, login_request.password, session)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials!")
    else:
        access_token = create_token(user.id)
        return {"access_token": access_token,  "token_type" : "bearer"}

@auth_router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": f"User {current_user.email} logged out succesfully!"}

@auth_router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = auth_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/google/authorize")
async def google_authorize(current_user: User = Depends(get_current_user)):
    state = create_token(current_user.id)
    authorization_url = calendar_service.get_authorization_url(state)
    return {"authorization_url": authorization_url}


@auth_router.get("/google/callback")
async def google_callback(code: str, state: str, session: Session = Depends(get_session)):
    try:
        user = get_current_user(token=state, session=session)

        credentials = calendar_service.exchange_code_for_tokens(code)

        user.google_refresh_token = credentials["refresh_token"]
        user.calendar_connected = True

        session.commit()
        session.refresh(user)
    except Exception:
        return RedirectResponse(f"{FRONTEND_URL}/?calendar=error")

    return RedirectResponse(f"{FRONTEND_URL}/?calendar=connected")

@auth_router.delete("/google/disconnect")
async def google_disconnect(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id==current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.google_refresh_token = None
    user.calendar_connected = False

    session.commit()
    session.refresh(user)
    return {"message": "Google Calendar disconnected successfully"}
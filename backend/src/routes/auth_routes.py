from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserRequest, LoginRequest
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(user_id):
    expire_date = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # JWT claims must be JSON-serializable: `exp` is a Unix timestamp (int) and
    # `sub` must be a string per the JWT spec.
    dic_info = {"sub": str(user_id), "exp": int(expire_date.timestamp())}

    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def auth_user(email: str, password: str, session: Session = Depends(get_session)):
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
        raise HTTPException(status_code=404, detail="User not found with email {login_request.email}!")
    else:
        access_token = create_token(user.id)
        return {"access_token": access_token,  "token_type" : "Bearer"}
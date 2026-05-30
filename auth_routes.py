from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas import UserRequest, LoginRequest
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(user_id):
    token = f"sci1909{user_id}"
    return token

@auth_router.get("/")
async def authenticate():
    """
    This is the standardt authentication route for the API
    """
    return {"message": "Authentication in process", "authenticated": False}

@auth_router.post("/create_user")
async def create_user(user_request: UserRequest, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==user_request.email).first()

    if user:
        raise HTTPException(status_code=400, details="Email alredy been used by another user!")
    else:
        encrypted_password = bcrypt_context.hash(user_request.password)
        new_user = User(user_request.name, user_request.email, encrypted_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {"message": "User {new_user.name} with email {new_user.email} created succesfully!"}
    
@auth_router.post("/login")
async def login(login_request: LoginRequest, session: Session = Depends(get_session)):
    user = session.querry(User).filter(User.email==login_request.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found with email {login_request.email}!")
    else:
        access_token = create_token(user.id)
        return {"access_token": access_token,  "token_type" : "Bearer"}
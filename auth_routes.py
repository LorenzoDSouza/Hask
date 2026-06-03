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

def auth_user(email: str, password: str, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==email).first()

    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.password):
        return False

    return user

@auth_router.get("/")
async def home():
    """
    This is the standardt authentication route for the API
    """
    return {"message": "You accessed the standardt auth route", "authenticated": False}



@auth_router.post("/users")
async def create_user(user_request: UserRequest, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==user_request.email).first()

    if user:
        raise HTTPException(status_code=400, details="Email alredy been used by another user!")
    
    encrypted_password = bcrypt_context.hash(user_request.password)
    new_user = User(user_request.name, user_request.email, encrypted_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User {new_user.name} with email {new_user.email} created successfully!"}



@auth_router.get("/users/{user_id}")
async def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found with id {user_id}!")
    
    return user



@auth_router.delete("/users/{user_id}")
async def delete_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Couldn't delete user because no user was found with Id {user_id}!")

    session.delete(user)
    session.commit()

    return {"message": "User deleted successfully!"}



@auth_router.put("/users/{user_id}")
async def update_user_by_id(user_id: int, user_request: UserRequest, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Couldn't delete user because no user was found with Id {user_id}!")

    user.name = user_request.name
    user.email = user_request.email

    encrypted_password = bcrypt_context.hash(user_request.password)

    user.password = encrypted_password

    session.commit()
    session.refresh(user)

    return user

@auth_router.post("/login")
async def login(login_request: LoginRequest, session: Session = Depends(get_session)):
    user = auth_user(login_request.email, login_request.password, session)

    if not user:
        raise HTTPException(status_code=404, detail="User not found with email {login_request.email}!")
    else:
        access_token = create_token(user.id)
        return {"access_token": access_token,  "token_type" : "Bearer"}
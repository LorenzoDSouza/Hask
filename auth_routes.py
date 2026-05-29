from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def authenticate():
    """
    This is the standardt authentication route for the API
    """
    return {"message": "Authentication in process", "authenticated": False}

@auth_router.post("/create_user")
async def create_user(email: str, password: str, name: str, session = Depends(get_session)):
    user = session.query(User).filter(User.email==email).first()

    if user:
        raise HTTPException(status_code=400, details="Email alredy been used by another user!")
    else:
        encrypted_password = bcrypt_context.hash(password)
        new_user = User(name, email, encrypted_password)
        session.add(new_user)
        session.commit()
        return {"message": "User {ame} with email {email} created succesfully!"}
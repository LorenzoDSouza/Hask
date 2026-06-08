from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_current_user, get_session
from main import bcrypt_context
from schemas import UserRequest
from sqlalchemy.orm import Session

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/", status_code=201)
async def create_user(user_request: UserRequest, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==user_request.email).first()

    if user:
        raise HTTPException(status_code=400, detail="Email alredy been used by another user!")
    
    encrypted_password = bcrypt_context.hash(user_request.password)
    new_user = User(user_request.name, user_request.email, encrypted_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": f"User {new_user.name} with email {new_user.email} created successfully!"}

@user_router.get("")
async def users(session: Session = Depends(get_session)):
    """
    This is the route to list all the users
    """
    return session.query(User).all()

@user_router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    This is the route to get the current logged-in user's information
    """
    return current_user

@user_router.get("/{user_id}")
async def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User not found with id {user_id}!")
    
    return user



@user_router.delete("/{user_id}", status_code=204)
async def delete_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"Couldn't delete user because no user was found with Id {user_id}!")

    session.delete(user)
    session.commit()

    return {"message": "User deleted successfully!"}



@user_router.put("/{user_id}")
async def update_user_by_id(user_id: int, user_request: UserRequest, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"Couldn't update user because no user was found with Id {user_id}!")

    existing_user = session.query(User).filter(User.email == user_request.email,User.id != user_id).first()
                     
    if existing_user:
        raise HTTPException(status_code=409, detail=f"Email {user_request.email} already in use!")
    
    user.name = user_request.name
    user.email = user_request.email

    encrypted_password = bcrypt_context.hash(user_request.password)

    user.password = encrypted_password

    session.commit()
    session.refresh(user)

    return user

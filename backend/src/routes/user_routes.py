from fastapi import APIRouter, Depends
from models import User
from dependencies import get_current_user, get_session
from schemas import UserRequest
from sqlalchemy.orm import Session
from src.services.user_service import UserService

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", status_code=201)
async def create_user(user_request: UserRequest, session: Session = Depends(get_session)):
    user = UserService(session).create_user(
        user_request.name, user_request.email, user_request.password
    )
    return {"message": f"User {user.name} with email {user.email} created successfully!"}


@user_router.get("/")
async def users(session: Session = Depends(get_session)):
    """List all the users."""
    return UserService(session).list_users()


@user_router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Return the current logged-in user's information."""
    return current_user


@user_router.get("/{user_id}")
async def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    return UserService(session).get_user(user_id)


@user_router.delete("/{user_id}", status_code=204)
async def delete_user_by_id(user_id: int, session: Session = Depends(get_session)):
    UserService(session).delete_user(user_id)


@user_router.put("/{user_id}")
async def update_user_by_id(
    user_id: int, user_request: UserRequest, session: Session = Depends(get_session)
):
    return UserService(session).update_user(
        user_id, user_request.name, user_request.email, user_request.password
    )

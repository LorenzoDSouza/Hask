from fastapi import APIRouter
from models import User, db
from sqlalchemy.orm import sessionmaker

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def authenticate():
    """
    This is the standardt authentication route for the API
    """
    return {"message": "Authentication in process", "authenticated": False}

@auth_router.post("/create_user")
async def create_user(email: str, password: str, name: str):
    Session = sessionmaker(bind=db)
    session = Session()
    user = session.query(User).filter(User.email==email).first()

    if user:
        return {"message": "Email alredy been used by another user!"}
    else:
        new_user = User(name, email, password)
        session.add(new_user)
        session.commit()
        return {"message": "User created succesfully!"}
from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTE"))

app = FastAPI() #no terminal pra rodar a api: uvicorn main:app --reload

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from repository.auth_routes import auth_router
from repository.task_routes import task_router
from repository.user_routes import user_router

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(user_router)
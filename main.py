from fastapi import FastAPI

app = FastAPI()
#no terminal pra rodar a api: uvicorn main:app --reload

from auth_routes import auth_router
from task_routes import task_router

app.include_router(auth_router)
app.include_router(task_router)
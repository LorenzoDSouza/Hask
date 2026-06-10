from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # no terminal pra rodar a api: uvicorn main:app --reload

# Allow the Vite frontend (localhost:5173) to call the API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.routes.auth_routes import auth_router
from src.routes.task_routes import task_router
from src.routes.user_routes import user_router

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(user_router)

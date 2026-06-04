from pydantic import BaseModel
from typing import Optional
from models import TaskStatus

class UserRequest(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True

class TaskRequest(BaseModel):
    title: str
    user_id: int
    category: str
    status: TaskStatus = TaskStatus.TODO
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
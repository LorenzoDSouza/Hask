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
    start_date_time: Optional[str] = None
    end_date_time: Optional[str] = None
    
    class Config:
        from_attributes = True

class UpdateTaskRequest(BaseModel):
    id: int
    title: Optional[str] = None
    user_id: Optional[int] = None
    category: Optional[str] = None
    status: Optional[TaskStatus] = None
    start_date_time: Optional[str] = None
    end_date_time: Optional[str] = None
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
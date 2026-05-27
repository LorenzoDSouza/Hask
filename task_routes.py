from fastapi import APIRouter

task_router = APIRouter(prefix="/tasks", tags=["tasks"])

@task_router.get("/")
async def tasks():
    """
    This is the route to list all the tasks
    """
    return {"message": "You accessed the tasks"}
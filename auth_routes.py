from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def authenticate():
    """
    This is the standardt authentication route for the API
    """
    return {"message": "Authentication in process", "authenticated": False}
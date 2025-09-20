from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def home():
    """
    This is the system's default auth route.
    """
    return {"message": "You ahve accessed the auth route", "authenticated": False}

from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def authenticate():
    return {"message": "You ahve accessed the auth route", "authenticated": False}

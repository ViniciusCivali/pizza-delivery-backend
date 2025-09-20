from email.policy import HTTP
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session
from app import User
from dependencies import hash_password, verify_password, UserSchema, LoginSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def create_token(user_id: str):
    return f"adfasdfasdf{user_id}"


@auth_router.get("/")
async def home():
    """
    This is the system's default auth route.
    """
    return {"message": "You ahve accessed the auth route", "authenticated": False}

# Receiving non-standard parameters


@auth_router.post("/create_user")
async def create_user(user_schema: UserSchema, session: Session = Depends(get_session)):
    """
    Create a user
    """

    if session.query(User).filter(User.email == user_schema.email).first():
        # The user already exist
        raise HTTPException(status_code=400, detail="User already exist")
    else:
        # Create user
        new_user = User(
            name=user_schema.name,
            email=user_schema.email,
            password=hash_password(user_schema.password)
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {"message": f"User {user_schema.name} created successfully"}

# login -> email and password -> token JWT (Json Web Token) afasgusfifjjvdkjv


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    """
    Login
    """
    user = session.query(User).filter(User.email == login_schema.email).first()

    if user:
        if verify_password(login_schema.password, user.password):
            access_token = create_token(user.id)

            return {
                "access_token": access_token,
                "token_type": "Bearer",
            }
        else:
            raise HTTPException(status_code=400, detail="Incorrect password")
    else:
        raise HTTPException(status_code=400, detail="User not found")

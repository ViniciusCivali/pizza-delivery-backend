from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session
from app import User
from dependencies import hash_password, verify_password, UserSchema, LoginSchema, create_access_token, create_refresh_token, verify_token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])


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


@staticmethod
def authenticate_user(session: Session, email: str, password: str) -> bool:
    user = session.query(User).filter(User.email == email).first()
    if user:
        if verify_password(password, user.password):
            return True
        else:
            raise HTTPException(status_code=400, detail="Wrong credentials")
    else:
        raise HTTPException(status_code=400, detail="User not found")


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    """
    Login
    """
    if authenticate_user(session, login_schema.email, login_schema.password):
        user = session.query(User).filter(
            User.email == login_schema.email).first()
        access_token = create_access_token(user_id=user.id)
        refresh_token = create_refresh_token(
            user_id=user.id, token_duration=timedelta(days=1))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }
    else:
        raise HTTPException(
            status_code=400, detail="email or password missmatch")


@auth_router.post("/login-form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    Login
    """
    if authenticate_user(session, form_data.username, form_data.password):
        user = session.query(User).filter(
            User.email == form_data.username).first()
        access_token = create_access_token(user_id=user.id)

        return {
            "access_token": access_token,
            "token_type": "Bearer",
        }
    else:
        raise HTTPException(
            status_code=400, detail="email or password missmatch")


@auth_router.post("/refresh")
async def user_refresh_token(user: User = Depends(verify_token)):
    access_token = create_access_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }

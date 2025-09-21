# core/security.py
from passlib.context import CryptContext

from dependencies import get_session
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login-form")


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt_context.verify(password, hashed)


def create_access_token(user_id: int, token_duration: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """ Create a JWT assigned with SECRET_KEY """
    dic_info = {
        "sub": f"{user_id}",
        "exp": (datetime.now(tz=timezone.utc) + token_duration).timestamp()
    }

    return jwt.encode(
        claims=dic_info, algorithm=ALGORITHM, key=SECRET_KEY)


def create_refresh_token(user_id: int, token_duration: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """ Refresh token """
    return create_access_token(user_id=user_id, token_duration=token_duration)


def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    """ Decode/verify a JWT """
    try:
        dic_info = jwt.decode(token=token,
                              key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(dic_info.get("sub"))
    except JWTError as error:
        print(error)
        raise HTTPException(
            status_code=401, detail="Access denied, check token validity")

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid access")
    return user

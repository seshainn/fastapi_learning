from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from src.config import Config
import jwt
import uuid
import logging

ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 15
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_data: dict, expiry: timedelta, refresh: bool = False):
    if expiry is not None:
    # Assumes expiry is already a timedelta or a datetime
        expiration = datetime.now(timezone.utc) + expiry if isinstance(expiry, timedelta) else expiry
    else:
        expiration = datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)

    payload = {
        "user": user_data,
        "exp": expiration,
        "jti": str(uuid.uuid4()),
        "refresh": refresh
    }
    token = jwt.encode(
        payload=payload, 
        key=Config.JWT_SECRET, 
        algorithm=Config.JWT_ALGORITHM, 
    )
    return token

def decode_access_token(token: str):
    try:
        token_data = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
    return token_data
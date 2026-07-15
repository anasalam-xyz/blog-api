from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_hash(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=30)
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta  # token will expire in 30 mins
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

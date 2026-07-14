from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)  # if i ever add newer schemes later, old bcrypt hashes still verify correctly, marked as "should rehash."


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_hash(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=30)
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta  # token will expire in 30 mins
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

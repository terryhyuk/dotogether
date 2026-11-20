
import os
import jwt

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from pwdlib import PasswordHash

load_dotenv()


# Password hashing
password_hash = PasswordHash.recommended()


def hash_password(pw: str) -> str:
    return password_hash.hash(pw)


def verify_password(pw: str, hashed: str) -> bool:
    return password_hash.verify(pw, hashed)


# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not configured")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Create JWT access token
def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# Verify and decode JWT access token
def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except jwt.InvalidTokenError:
        return None

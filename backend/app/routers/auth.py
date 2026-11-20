from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.utils.security import (verify_password, create_access_token, decode_access_token)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.Token)
def login(req: schemas.UserLogin, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(models.User).filter(
        models.User.email == req.email
    ).first()

    # Verify password
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT access token
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload["sub"])

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

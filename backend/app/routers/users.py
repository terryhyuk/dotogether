from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.utils.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=schemas.UserOut)
def signup(req: schemas.UserCreate, db: Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.email == req.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        email=req.email,
        password_hash=hash_password(req.password),
        name=req.name,
        department=req.department,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.UserOut)
def login(req: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or user.password_hash != hash_password(req.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@router.get("", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.dependencies import get_current_user
from app.utils.security import hash_password
from fastapi import HTTPException
from app.schemas.user import UserCreate, UserLogin
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token

router = APIRouter()


@router.get("/test")
def test():
    return {"message": "Auth route working"}


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )
    
    token = create_access_token(
    {"sub": str(existing_user.id)}
    )

    return {
    "access_token": token,
    "token_type": "bearer"
    } 

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "message": "Protected route accessed",
        "user": current_user
    }
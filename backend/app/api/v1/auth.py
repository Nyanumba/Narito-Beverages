from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from ...models.users import User 
from ...schemas.user import UserCreate, UserResponse, UserLogin
from datetime import timedelta

from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.core.email_utilis import send_verification_email

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# REGISTER
# -------------------------------
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email or phone already exists
    existing_user = db.query(User).filter(
        (User.email == user.email) |
        (User.phone_number == user.phone_number)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or phone already registered")

    hashed_pw = hash_password(user.password)
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send verification email
    token = create_access_token(
        {"sub": user.email},
        expires_delta=timedelta(minutes=60)
    )
    send_verification_email(user.email, token)

    return new_user
# -------------------------------
# EMAIL VERIFICATION
# -------------------------------
@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    user.is_active = True
    db.commit()

    return {"message": "Email verified successfully. You can now log in."}

# -------------------------------
# LOGIN
# -------------------------------
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not db_user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email before logging in")

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

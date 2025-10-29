from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# === User Schemas ===

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None  


class UserCreate(UserBase):
    password: str  
    phone_number: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str  


class UserResponse(UserBase):
    id: int
    phone_number: str
    is_verified: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # ← Correct for Pydantic v2
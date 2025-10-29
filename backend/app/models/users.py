#from pydantic import Base, Field, EmailStr
from typing import Optional
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column (Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True, nullable = False)
    full_name = Column (String, unique = False, index = True, nullable = False)
    hashed_password = Column(String, nullable=False)
    phone_number = Column (String, unique = True, index = True, nullable = False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    

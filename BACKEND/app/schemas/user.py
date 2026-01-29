from pydantic import BaseModel, EmailStr
from typing import Optional
from app.enums.role import RoleEnum

class UserCreate(BaseModel):
    nom: str
    email: EmailStr
    password: str
    role: Optional[RoleEnum] = None

class UserUpdate(BaseModel):
    nom: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None

class UserResponse(BaseModel):
    id: int
    nom: str
    email: str
    role: RoleEnum

    class Config:
        from_attributes = True

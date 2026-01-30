from pydantic import BaseModel, EmailStr
from app.enums.role import RoleEnum


class UserCreate(BaseModel):
    nom: str
    email: EmailStr
    password: str
    role: RoleEnum | None = None


class UserUpdate(BaseModel):
    nom: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: RoleEnum | None = None


class UserResponse(BaseModel):
    id: int
    nom: str
    email: str
    role: RoleEnum

    class Config:
        from_attributes = True

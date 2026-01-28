from pydantic import BaseModel
from app.enums.role import RoleEnum

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: RoleEnum

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum

    class Config:
        from_attributes = True

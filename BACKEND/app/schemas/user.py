from pydantic import BaseModel, EmailStr, ConfigDict
from app.enums.role import RoleEnum


class UserCreate(BaseModel):
    nom: str
    email: EmailStr
    password: str
    role: RoleEnum | None = None


# Schéma pour la mise à jour par un utilisateur normal (email et password uniquement)
class UserUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid') # Rejette les champs non autorisés
    email: EmailStr | None = None
    password: str | None = None


# Schéma pour la mise à jour par un administrateur (tous les champs)
class UserUpdateAdmin(BaseModel):
    nom: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: RoleEnum | None = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int # généré automatiquement après la création
    nom: str
    email: str
    role: RoleEnum

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Schéma pour la requête de connexion."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schéma pour la réponse contenant le token."""
    access_token: str
    token_type: str = "bearer"
    user: dict


class PasswordChange(BaseModel):
    """Schéma pour changer le mot de passe."""
    old_password: str
    new_password: str

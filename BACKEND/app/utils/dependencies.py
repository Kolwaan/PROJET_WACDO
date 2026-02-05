from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.utils.jwt import decode_access_token
from app.utils.hash import verify_password
from app.models.user import User
from app.enums.role import RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    
    # Décode et valide le token
    payload = decode_access_token(token)
    
    # Extraction des données
    email: str = payload.get("sub")
    role: str = payload.get("role")
    user_id: int = payload.get("user_id")
    
    # Vérification que l'email est présent (champ obligatoire)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide : email manquant dans le payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "email": email,
        "role": role,
        "user_id": user_id
    }


def require_role(*allowed_roles: RoleEnum):

    def role_checker(current_user: dict = Depends(get_current_user)):
        """Fonction interne qui vérifie le rôle."""
        user_role = current_user.get("role")
        
        # Vérification du rôle
        if user_role not in [role.value for role in allowed_roles]:
            roles_str = ", ".join([r.value for r in allowed_roles])
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès refusé. Rôles autorisés : {roles_str}. Votre rôle : {user_role}"
            )
        
        # Retourne current_user si le rôle est bon
        return current_user
    
    return role_checker


def authenticate_user(db: Session, email: str, password: str) -> User | None:

    # Recherche de l'utilisateur par email
    user = db.query(User).filter(User.email == email).first()
    
    # Si l'utilisateur n'existe pas
    if not user:
        return None
    
    # Vérification du mot de passe
    if not verify_password(password, user.password):
        return None
    
    # Authentification réussie
    return user


def get_current_active_user(
    current_user: dict = Depends(get_current_user),
    db: Session = None
) -> User:
    user_id = current_user["user_id"]
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable en base de données"
        )
    
    return user

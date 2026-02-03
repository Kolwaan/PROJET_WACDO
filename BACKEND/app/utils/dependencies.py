from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.utils.jwt import decode_access_token
from app.utils.hash import verify_password
from app.models.user import User
from app.enums.role import RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth_routes/token")


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
    """
    Crée une dépendance qui vérifie si l'utilisateur a un des rôles autorisés.
    
    Cette fonction retourne une autre fonction (closure) qui sera utilisée
    comme dépendance FastAPI.
    
    Args:
        *allowed_roles: Un ou plusieurs rôles autorisés (RoleEnum)
    
    Returns:
        Fonction de dépendance qui vérifie les permissions
    
    Raises:
        HTTPException(403): Si l'utilisateur n'a pas le bon rôle
        
    Example:
        ```python
        from app.enums.role import RoleEnum
        
        # Route accessible uniquement aux administrateurs
        @router.delete("/users/{user_id}")
        async def delete_user(
            user_id: int,
            current_user: dict = Depends(require_role(RoleEnum.ADMINISTRATEUR))
        ):
            # current_user est disponible si le rôle est bon
            return {"message": "User deleted"}
        
        # Route accessible aux préparateurs ET superviseurs
        @router.put("/orders/{order_id}/status")
        async def update_order_status(
            order_id: int,
            current_user: dict = Depends(require_role(
                RoleEnum.AGENT_DE_PREPARATION,
                RoleEnum.SUPERVISEUR_DE_PREPARATION,
                RoleEnum.ADMINISTRATEUR
            ))
        ):
            return {"message": "Status updated"}
        
        # Ou avec dependencies (sans utiliser current_user)
        @router.get(
            "/admin/dashboard",
            dependencies=[Depends(require_role(RoleEnum.ADMINISTRATEUR))]
        )
        async def admin_dashboard():
            # Pas besoin de current_user dans la signature
            return {"message": "Admin dashboard"}
        ```
        
    Note:
        - Si plusieurs rôles sont autorisés, il suffit d'en avoir UN
        - L'administrateur peut avoir accès à tout en ajoutant son rôle partout
        - Cette fonction retourne current_user pour pouvoir l'utiliser
    """
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


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authentifie un utilisateur avec son email et mot de passe.
    
    Cette fonction :
    1. Recherche l'utilisateur par email
    2. Vérifie le mot de passe avec verify_password (Argon2)
    3. Retourne l'utilisateur si tout est correct
    
    Args:
        db: Session de base de données SQLAlchemy
        email: Email de l'utilisateur
        password: Mot de passe en clair
    
    Returns:
        Objet User si l'authentification réussit, None sinon
        
    Example:
        ```python
        from app.database import SessionLocal
        
        db = SessionLocal()
        user = authenticate_user(db, "admin@wacdo.com", "password123")
        
        if user:
            print(f"Bienvenue {user.nom}")
        else:
            print("Identifiants incorrects")
        ```
        
    Note:
        - Cette fonction ne lève PAS d'exception
        - Elle retourne None si l'email ou le mot de passe est incorrect
        - C'est à la route d'appel de gérer l'erreur
    """
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
    """
    Récupère l'utilisateur actuel depuis la base de données.
    
    À utiliser si vous avez besoin de l'objet User complet (pas juste le dict).
    
    Args:
        current_user: Utilisateur du token (via get_current_user)
        db: Session de base de données
        
    Returns:
        Objet User complet
        
    Raises:
        HTTPException(404): Si l'utilisateur n'existe plus en base
        
    Example:
        ```python
        @router.get("/me/full")
        def get_full_profile(
            user: User = Depends(get_current_active_user),
            db: Session = Depends(get_db)
        ):
            return {
                "id": user.id,
                "nom": user.nom,
                "email": user.email,
                "role": user.role
            }
        ```
    """
    user_id = current_user["user_id"]
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable en base de données"
        )
    
    return user

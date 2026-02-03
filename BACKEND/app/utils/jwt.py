from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, status

from app.utils.settings import settings


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:

    # Copie des données pour ne pas modifier l'original
    to_encode = data.copy()
    
    # Calcul de la date d'expiration
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Ajout de l'expiration dans le payload
    to_encode.update({"exp": expire})
    
    # Encodage du token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        # Décodage et validation automatique
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
        
    except jwt.ExpiredSignatureError:
        # Token expiré
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré. Veuillez vous reconnecter.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    except jwt.InvalidTokenError as e:
        # Token invalide (signature incorrecte, format invalide, etc.)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalide : {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def decode_token_without_validation(token: str) -> dict:
    try:
        # options={"verify_signature": False} désactive toutes les vérifications
        payload = jwt.decode(
            token,
            options={"verify_signature": False}
        )
        return payload
    except Exception as e:
        return {"error": str(e)}


def get_token_expiration(token: str) -> datetime | None:
    try:
        payload = decode_token_without_validation(token)
        exp_timestamp = payload.get("exp")
        
        if exp_timestamp:
            return datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        return None
        
    except Exception:
        return None


def is_token_expired(token: str) -> bool:
    try:
        decode_access_token(token)
        return False
    except HTTPException as e:
        if "expiré" in str(e.detail).lower():
            return True
        return False

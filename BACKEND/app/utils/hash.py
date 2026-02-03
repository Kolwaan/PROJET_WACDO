from passlib.context import CryptContext
from app.utils.settings import settings


# Configuration du contexte de hachage Argon2
pwd_context = CryptContext(
    schemes=["argon2"],  # Utilise Argon2id (variant le plus sécurisé)
    deprecated="auto",    # Migre automatiquement les anciens hashs
    
    # Paramètres Argon2 (configurable via settings)
    argon2__time_cost=settings.ARGON2_TIME_COST,        # Itérations
    argon2__memory_cost=settings.ARGON2_MEMORY_COST,    # Mémoire (KB)
    argon2__parallelism=settings.ARGON2_PARALLELISM,    # Threads
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def needs_update(hashed_password: str) -> bool:
    return pwd_context.needs_update(hashed_password)


# info debug
def get_hash_info(hashed_password: str) -> dict:
    try:
        return pwd_context.identify(hashed_password, resolve=True)
    except Exception:
        return {"error": "Invalid hash format"}

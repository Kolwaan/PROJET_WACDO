from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    # JWT Configuration
    SECRET_KEY: str = "PA3vb088_vz78dN4lDR4tg88bQ3O4-hFEXu0CAKWfHY"
    ALGORITHM: str = "HS256"    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DATABASE_URL: str = "sqlite:///./base_de_donnees.db"

    
    APP_NAME: str = "Backend FastAPI Wacdo"
    
    DEBUG: bool = False
    # Mode debug
    # True : Affiche les erreurs détaillées (développement)
    # False : Masque les détails (production)
    
    ENVIRONMENT: str = "development"
    
    # CORS Configuration
    ALLOWED_ORIGINS: list[str] = ["*"]
    
    # Security Configuration
    ARGON2_TIME_COST: int = 3
    # Nombre d'itérations pour Argon2 (plus = plus sécurisé mais plus lent)
    
    ARGON2_MEMORY_COST: int = 65536
    ARGON2_PARALLELISM: int = 4


    # Pydantic Configuration
    model_config = SettingsConfigDict(
        env_file=".env",              # Lit automatiquement le fichier .env
        env_file_encoding="utf-8",    # Encodage du fichier
        case_sensitive=False,         # SECRET_KEY fonctionne
        extra="ignore"                # Ignore les variables d'env inconnues
    )


# Instance singleton des settings
settings = Settings()


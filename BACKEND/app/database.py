import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Charger le .env directement, sans passer par settings
# (évite l'import circulaire : database → settings → dependencies → models → database)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./base_de_donnees.db")

# Render fournit des URLs "postgres://" (ancien format), SQLAlchemy attend "postgresql://"
# On corrige aussi pour utiliser le driver psycopg3 en production
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# Configuration adaptée selon le type de base de données
if DATABASE_URL.startswith("sqlite"):
    # SQLite pour le développement local
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL pour la production (Render)
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Vérifie la connexion avant utilisation
        pool_size=10,        # Nombre de connexions maintenues
        max_overflow=20      # Connexions supplémentaires en cas de pic
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    """
    Générateur de session de base de données.
    À utiliser avec Depends() dans FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
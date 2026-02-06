import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.utils.jwt import create_access_token
from app.enums.role import RoleEnum


# ==========================================
# Configuration de la base de données de test
# ==========================================

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override de la dépendance get_db pour utiliser la DB de test."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# ==========================================
# Fixtures principales
# ==========================================

@pytest.fixture(scope="function")
def db_session():
    """
    Crée une base de données propre pour chaque test.
    Utilise scope="function" pour recréer la DB à chaque test.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Client de test FastAPI avec la base de données de test.
    """
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# ==========================================
# Fixtures pour les tokens JWT
# ==========================================

@pytest.fixture
def admin_token():
    """Token JWT pour un administrateur."""
    return create_access_token({
        "sub": "admin@test.com",
        "role": RoleEnum.ADMINISTRATEUR.value,
        "user_id": 1
    })


@pytest.fixture
def superviseur_token():
    """Token JWT pour un superviseur de préparation."""
    return create_access_token({
        "sub": "superviseur@test.com",
        "role": RoleEnum.SUPERVISEUR_DE_PREPARATION.value,
        "user_id": 2
    })


@pytest.fixture
def preparateur_token():
    """Token JWT pour un agent de préparation."""
    return create_access_token({
        "sub": "preparateur@test.com",
        "role": RoleEnum.AGENT_DE_PREPARATION.value,
        "user_id": 3
    })


@pytest.fixture
def accueil_token():
    """Token JWT pour un agent d'accueil."""
    return create_access_token({
        "sub": "accueil@test.com",
        "role": RoleEnum.AGENT_ACCUEIL.value,
        "user_id": 4
    })


@pytest.fixture
def preparateur_2_token():
    """Token JWT pour un deuxième agent de préparation (pour tester les restrictions)."""
    return create_access_token({
        "sub": "preparateur2@test.com",
        "role": RoleEnum.AGENT_DE_PREPARATION.value,
        "user_id": 5
    })


# ==========================================
# Fixtures utilitaires
# ==========================================

@pytest.fixture
def auth_headers():
    """
    Fonction helper pour créer des headers d'authentification.
    Usage: auth_headers(admin_token)
    """
    def _auth_headers(token: str):
        return {"Authorization": f"Bearer {token}"}
    return _auth_headers

# Créer un compte
@pytest.fixture
def sample_user_data():
    return {
        "nom": "Test",
        "email": "test@example.com",
        "password": "Password123!",
        "role": RoleEnum.AGENT_ACCUEIL.value
    }

# Créer un produit
@pytest.fixture
def sample_product_data():
    return {
        "nom": "Big Mac",
        "description": "Le burger classique de McDonald's",
        "prixHT": 5.50,           
        "type": "PRODUIT_UNIQUE",         
        "disponibilite": True,    
        "image": "bigmac.png",    
        "options": []             
    }


# Créer un menu.
@pytest.fixture
def sample_menu_data():
    return {
        "nom": "Menu Best Of",
        "description": "Le meilleur menu du moment",
        "prixHT": 8.50,           
        "menu_type": "BEST_OF",   
        "disponibilite": True,    
        "image": "bestof.png",    
        "product_ids": []
    }

# Créer une commande
@pytest.fixture
def sample_order_data():
    return {
        "chevalet": 456,
        "sur_place": True,
        "product_ids": [1],
        "menu_ids": [1],
        "preparateur_id": 1
        }
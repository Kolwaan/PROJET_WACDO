from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import user_routes, product_routes, menu_routes, order_routes, auth_routes
from app.database import Base, engine
from app.utils.settings import settings

# Créer les tables dans la base de données (utilise Alembic en production)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Backend FastAPI Wacdo",
    description="API de gestion pour l'application WACDO",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Configuration CORS — ALLOWED_ORIGINS est déjà une list[str] grâce à Pydantic
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routes
app.include_router(auth_routes.router)  # Routes d'authentification
app.include_router(user_routes.router)
app.include_router(product_routes.router)
app.include_router(menu_routes.router)
app.include_router(order_routes.router)


@app.get("/")
def root():
    """
    Route racine - Vérification que l'API est en ligne
    """
    return {
        "message": "API WACDO en ligne",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "endpoints": {
            "auth": "/auth",
            "users": "/users",
            "products": "/products",
            "menus": "/menus",
            "orders": "/orders",
            "docs": "/docs" if settings.ENVIRONMENT == "development" else "Disabled in production",
        }
    }


@app.get("/health")
def health_check():
    """
    Health check pour Render
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }
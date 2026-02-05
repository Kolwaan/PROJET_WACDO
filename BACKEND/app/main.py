from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import user_routes, product_routes, menu_routes, order_routes, auth_routes
from app.database import Base, engine

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Backend FastAPI Wacdo",
    description="API de gestion pour l'application WACDO"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {
        "message": "API WACDO en ligne",
        "endpoints": {
            "auth": "/auth",
            "users": "/users",
            "products": "/products",
            "menus": "/menus",
            "orders": "/orders",
        }
    }

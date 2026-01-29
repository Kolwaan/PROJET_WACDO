from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.controllers.product_controller import (
    create_product,
    get_all_products,
    get_product_by_id,
    get_products_by_type,
    get_available_products,
    update_product,
    delete_product,
    toggle_availability
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product_route(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Créer un nouveau produit"""
    return create_product(db, product)


@router.get("/", response_model=list[ProductResponse])
def read_products(db: Session = Depends(get_db)):
    """Récupérer tous les produits"""
    return get_all_products(db)


@router.get("/available", response_model=list[ProductResponse])
def read_available_products(db: Session = Depends(get_db)):
    """Récupérer uniquement les produits disponibles"""
    return get_available_products(db)


@router.get("/type/{product_type}", response_model=list[ProductResponse])
def read_products_by_type(product_type: str, db: Session = Depends(get_db)):
    """Récupérer les produits par type"""
    return get_products_by_type(db, product_type)


@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """Récupérer un produit par ID"""
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product_route(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un produit"""
    product = update_product(db, product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product


@router.patch("/{product_id}/toggle-availability", response_model=ProductResponse)
def toggle_product_availability(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Basculer la disponibilité d'un produit"""
    product = toggle_availability(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    """Supprimer un produit"""
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

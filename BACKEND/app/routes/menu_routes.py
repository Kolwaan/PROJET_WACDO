from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.schemas.menu import MenuCreate, MenuUpdate, MenuResponse, MenuWithProductsResponse
from app.controllers.menu_controller import (
    create_menu,
    get_all_menus,
    get_menu_by_id,
    get_menus_by_type,
    get_available_menus,
    update_menu,
    delete_menu,
    toggle_availability,
    add_products_to_menu,
    remove_products_from_menu
)


router = APIRouter(
    prefix="/menus",
    tags=["Menus"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=MenuResponse,
    status_code=status.HTTP_201_CREATED
)
def create_menu_route(
    menu: MenuCreate,
    db: Session = Depends(get_db)
):
    """Créer un nouveau menu"""
    return create_menu(db, menu)


@router.get("/", response_model=list[MenuResponse])
def read_menus(db: Session = Depends(get_db)):
    """Récupérer tous les menus"""
    return get_all_menus(db)


@router.get("/available", response_model=list[MenuResponse])
def read_available_menus(db: Session = Depends(get_db)):
    """Récupérer uniquement les menus disponibles"""
    return get_available_menus(db)


@router.get("/type/{menu_type}", response_model=list[MenuResponse])
def read_menus_by_type(menu_type: str, db: Session = Depends(get_db)):
    """Récupérer les menus par type"""
    return get_menus_by_type(db, menu_type)


@router.get("/{menu_id}", response_model=MenuResponse)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    """Récupérer un menu par ID"""
    menu = get_menu_by_id(db, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return menu


@router.put("/{menu_id}", response_model=MenuResponse)
def update_menu_route(
    menu_id: int,
    menu_data: MenuUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un menu"""
    menu = update_menu(db, menu_id, menu_data)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return menu


@router.patch("/{menu_id}/toggle-availability", response_model=MenuResponse)
def toggle_menu_availability(
    menu_id: int,
    db: Session = Depends(get_db)
):
    """Basculer la disponibilité d'un menu"""
    menu = toggle_availability(db, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return menu


@router.post("/{menu_id}/products", response_model=MenuResponse)
def add_products_route(
    menu_id: int,
    product_ids: List[int],
    db: Session = Depends(get_db)
):
    """Ajouter des produits à un menu"""
    menu = add_products_to_menu(db, menu_id, product_ids)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return menu


@router.delete("/{menu_id}/products", response_model=MenuResponse)
def remove_products_route(
    menu_id: int,
    product_ids: List[int],
    db: Session = Depends(get_db)
):
    """Retirer des produits d'un menu"""
    menu = remove_products_from_menu(db, menu_id, product_ids)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return menu


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_route(menu_id: int, db: Session = Depends(get_db)):
    """Supprimer un menu"""
    success = delete_menu(db, menu_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu non trouvé")

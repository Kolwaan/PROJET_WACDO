from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.order import (
    OrderCreate, 
    OrderUpdate, 
    OrderResponse, 
    OrderWithDetailsResponse,
    OrderStatusUpdate
)
from app.controllers.order_controller import (
    create_order,
    get_all_orders,
    get_order_by_id,
    get_orders_by_status,
    get_orders_by_preparateur,
    get_orders_sur_place,
    get_orders_a_emporter,
    update_order,
    update_order_status,
    assign_preparateur,
    delete_order,
    get_order_total
)
from app.enums.statut import OrderStatus


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=OrderWithDetailsResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order_route(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle commande"""
    return create_order(db, order)


@router.get("/", response_model=list[OrderWithDetailsResponse])
def read_orders(db: Session = Depends(get_db)):
    """Récupérer toutes les commandes avec leurs détails (produits, menus)"""
    return get_all_orders(db)


@router.get("/status/{order_status}", response_model=list[OrderWithDetailsResponse])
def read_orders_by_status(order_status: OrderStatus, db: Session = Depends(get_db)):
    """Récupérer les commandes par statut avec leurs détails"""
    return get_orders_by_status(db, order_status)


@router.get("/preparateur/{preparateur_id}", response_model=list[OrderWithDetailsResponse])
def read_orders_by_preparateur(preparateur_id: int, db: Session = Depends(get_db)):
    """Récupérer les commandes d'un préparateur avec leurs détails"""
    return get_orders_by_preparateur(db, preparateur_id)


@router.get("/sur-place", response_model=list[OrderWithDetailsResponse])
def read_orders_sur_place(db: Session = Depends(get_db)):
    """Récupérer les commandes sur place avec leurs détails"""
    return get_orders_sur_place(db)


@router.get("/a-emporter", response_model=list[OrderWithDetailsResponse])
def read_orders_a_emporter(db: Session = Depends(get_db)):
    """Récupérer les commandes à emporter avec leurs détails"""
    return get_orders_a_emporter(db)


@router.get("/{order_id}", response_model=OrderWithDetailsResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    """Récupérer une commande par ID avec tous ses détails"""
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order


@router.get("/{order_id}/total")
def get_total(order_id: int, db: Session = Depends(get_db)):
    """Obtenir le total TTC d'une commande"""
    total = get_order_total(db, order_id)
    if total is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return {"order_id": order_id, "total_ttc": total}


@router.put("/{order_id}", response_model=OrderWithDetailsResponse)
def update_order_route(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une commande"""
    order = update_order(db, order_id, order_data)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order


@router.patch("/{order_id}/status", response_model=OrderWithDetailsResponse)
def update_status_route(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour le statut d'une commande"""
    order = update_order_status(db, order_id, status_data.statut)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order


@router.patch("/{order_id}/assign/{preparateur_id}", response_model=OrderWithDetailsResponse)
def assign_preparateur_route(
    order_id: int,
    preparateur_id: int,
    db: Session = Depends(get_db)
):
    """Assigner un préparateur à une commande"""
    order = assign_preparateur(db, order_id, preparateur_id)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_route(order_id: int, db: Session = Depends(get_db)):
    """Supprimer une commande"""
    success = delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.enums.statut import OrderStatus

class OrderBase(BaseModel):
    chevalet: Optional[int] = None
    sur_place: bool = True

class OrderCreate(OrderBase):
    product_ids: Optional[List[int]] = []  # IDs des produits
    menu_ids: Optional[List[int]] = []  # IDs des menus
    preparateur_id: Optional[int] = None

class OrderUpdate(BaseModel):
    chevalet: Optional[int] = None
    sur_place: Optional[bool] = None
    statut: Optional[OrderStatus] = None
    preparateur_id: Optional[int] = None
    product_ids: Optional[List[int]] = None
    menu_ids: Optional[List[int]] = None

class OrderResponse(OrderBase):
    id: int
    date: datetime
    statut: OrderStatus
    preparateur_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class OrderWithDetailsResponse(OrderResponse):
    """Commande avec les détails (produits et menus)"""
    produits: List[dict] = []
    menus: List[dict] = []
    total_ttc: Optional[float] = None

class OrderStatusUpdate(BaseModel):
    """Pour mettre à jour uniquement le statut"""
    statut: OrderStatus

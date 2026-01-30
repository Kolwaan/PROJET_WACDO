from pydantic import BaseModel, Field
from datetime import datetime
from app.enums.statut import OrderStatus


class OrderBase(BaseModel):
    chevalet: int | None = None
    sur_place: bool = True


class OrderCreate(OrderBase):
    product_ids: list[int] | None = Field(default_factory=list)
    menu_ids: list[int] | None = Field(default_factory=list)
    preparateur_id: int | None = None


class OrderUpdate(BaseModel):
    chevalet: int | None = None
    sur_place: bool | None = None
    statut: OrderStatus | None = None
    preparateur_id: int | None = None
    product_ids: list[int] | None = None
    menu_ids: list[int] | None = None


class OrderResponse(OrderBase):
    id: int
    date: datetime
    statut: OrderStatus
    preparateur_id: int | None = None

    class Config:
        from_attributes = True


class OrderWithDetailsResponse(OrderResponse):
    """Commande avec les détails (produits et menus)"""
    produits: list[dict] = Field(default_factory=list)
    menus: list[dict] = Field(default_factory=list)
    total_ttc: float | None = None


class OrderStatusUpdate(BaseModel):
    """Pour mettre à jour uniquement le statut"""
    statut: OrderStatus

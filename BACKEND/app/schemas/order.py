from pydantic import BaseModel, Field
from datetime import datetime
from app.enums.statut import OrderStatus
from app.enums.type import ProductType
from app.enums.menu_type import MenuType


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


# Schémas pour les détails dans les commandes
class ProductInOrder(BaseModel):
    """Produit tel qu'il apparaît dans une commande"""
    id: int
    nom: str
    description: str | None = None
    prixHT: float
    image: str | None = None
    type: ProductType
    disponibilite: bool

    class Config:
        from_attributes = True


class ProductInMenuInOrder(BaseModel):
    """Produit dans un menu (pour l'affichage dans une commande)"""
    id: int
    nom: str
    description: str | None = None
    prixHT: float
    image: str | None = None
    type: ProductType

    class Config:
        from_attributes = True


class MenuInOrder(BaseModel):
    """Menu tel qu'il apparaît dans une commande, avec ses produits"""
    id: int
    nom: str
    description: str | None = None
    prixHT: float
    image: str | None = None
    menu_type: MenuType | None = None
    disponibilite: bool
    produits: list[ProductInMenuInOrder] = Field(default_factory=list)

    class Config:
        from_attributes = True


class PreparateurInfo(BaseModel):
    """Informations du préparateur"""
    id: int
    nom: str
    email: str
    role: str  # RoleEnum as string

    class Config:
        from_attributes = True


class OrderWithDetailsResponse(OrderResponse):
    """Commande avec tous les détails (produits, menus avec leurs produits, préparateur)"""
    produits: list[ProductInOrder] = Field(default_factory=list)
    menus: list[MenuInOrder] = Field(default_factory=list)
    preparateur: PreparateurInfo | None = None
    total_ttc: float | None = None

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """Pour mettre à jour uniquement le statut"""
    statut: OrderStatus

from pydantic import BaseModel, Field
from app.enums.menu_type import MenuType


class MenuBase(BaseModel):
    nom: str
    description: str | None = None
    prixHT: float
    image: str | None = None
    disponibilite: bool = True
    menu_type: MenuType | None = None


class MenuCreate(MenuBase):
    product_ids: list[int] | None = Field(default_factory=list)
    # ID des produits à associer lors de la création


class MenuUpdate(BaseModel):
    nom: str | None = None
    description: str | None = None
    prixHT: float | None = None
    image: str | None = None
    disponibilite: bool | None = None
    menu_type: MenuType | None = None
    product_ids: list[int] | None = None


class MenuResponse(MenuBase):
    id: int

    class Config:
        from_attributes = True


# Schéma pour les produits dans la réponse
class ProductInMenu(BaseModel):
    id: int
    nom: str
    description: str | None = None
    prixHT: float
    image: str | None = None
    disponibilite: bool
    type: str  # ProductType as string

    class Config:
        from_attributes = True


class MenuWithProductsResponse(MenuBase):
    """Menu avec la liste complète des produits inclus"""
    id: int
    produits: list[ProductInMenu] = Field(default_factory=list)

    class Config:
        from_attributes = True
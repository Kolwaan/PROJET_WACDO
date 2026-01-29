from pydantic import BaseModel
from typing import Optional, List
from app.enums.menu_type import MenuType

class MenuBase(BaseModel):
    nom: str
    description: Optional[str] = None
    prixHT: float
    image: Optional[str] = None
    disponibilite: bool = True
    menu_type: Optional[MenuType] = None

class MenuCreate(MenuBase):
    product_ids: Optional[List[int]] = []  # IDs des produits à associer

class MenuUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    prixHT: Optional[float] = None
    image: Optional[str] = None
    disponibilite: Optional[bool] = None
    menu_type: Optional[MenuType] = None
    product_ids: Optional[List[int]] = None

class MenuResponse(MenuBase):
    id: int
    
    class Config:
        from_attributes = True

class MenuWithProductsResponse(MenuResponse):
    """Menu avec les produits inclus"""
    produits: List[dict] = []

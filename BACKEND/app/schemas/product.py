from pydantic import BaseModel
from typing import Optional, List
from app.enums.type import ProductType

class ProductBase(BaseModel):
    nom: str
    description: Optional[str] = None
    prixHT: float
    image: Optional[str] = None
    options: Optional[List[str]] = []
    disponibilite: bool = True
    type: ProductType

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    prixHT: Optional[float] = None
    image: Optional[str] = None
    options: Optional[List[str]] = None
    disponibilite: Optional[bool] = None
    type: Optional[ProductType] = None

class ProductResponse(ProductBase):
    id: int
    
    class Config:
        from_attributes = True

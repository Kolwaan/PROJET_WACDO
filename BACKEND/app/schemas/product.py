from pydantic import BaseModel, Field
from app.enums.type import ProductType


class ProductBase(BaseModel):
    nom: str
    description: str | None = None
    prixHT: float
    image: str | None = None
    options: list[str] | None = Field(default_factory=list)
    disponibilite: bool = True
    type: ProductType


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    nom: str | None = None
    description: str | None = None
    prixHT: float | None = None
    image: str | None = None
    options: list[str] | None = None
    disponibilite: bool | None = None
    type: ProductType | None = None


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True

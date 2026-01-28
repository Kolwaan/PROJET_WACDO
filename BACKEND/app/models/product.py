from sqlalchemy import Column, Integer, String, Numeric, Boolean, Enum, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base
from app.enums.type import ProductType

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    description = Column(String)
    prixHT = Column(Numeric(10, 2))
    image = Column(String)
    options = Column(ARRAY(String))
    disponibilite = Column(Boolean, default=True)
    type = Column(Enum(ProductType), nullable=False)

    menus = relationship(
        "Menu",
        secondary="menu_products",
        back_populates="produits"
    )


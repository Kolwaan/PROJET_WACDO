from sqlalchemy import Column, Integer, String, Numeric, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    description = Column(String)
    prixHT = Column(Numeric(10, 2))
    image = Column(String)
    disponibilite = Column(Boolean, default=True)

    produits = relationship(
        "Product",
        secondary="menu_products",
        back_populates="menus"
    )

from sqlalchemy import Column, Integer, String, Numeric, Boolean, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.enums.menu_type import MenuType

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
    
    menu_type = Column(Enum(MenuType))

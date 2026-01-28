from sqlalchemy import Column, Integer, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base
from app.enums.statut import OrderStatus

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    chevalet = Column(Integer, nullable=True)
    sur_place = Column(Boolean, default=True)
    statut = Column(Enum(OrderStatus), default=OrderStatus.EN_COURS_PREPARATION)

    preparateur_id = Column(Integer, ForeignKey("users.id"))

    preparateur = relationship("User")
    produits = relationship("Product", secondary="order_products")
    menus = relationship("Menu", secondary="order_menus")
    
    def total_ttc(self, tva_rate=0.20):
        total_ht = 0
        
        # Somme des produits
        for product in self.produits:
            total_ht += float(product.prixHT)
        
        # Somme des menus
        for menu in self.menus:
            total_ht += float(menu.prixHT)
        
        return total_ht * (1 + tva_rate)

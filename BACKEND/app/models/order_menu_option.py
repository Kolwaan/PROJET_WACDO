from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

# Table d'association pour stocker les OPTIONS choisies pour chaque menu dans une commande
# Options = frites/potatoes + boisson choisie
order_menu_options = Table(
    "order_menu_options",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", Integer, ForeignKey("orders.id"), nullable=False),
    Column("menu_id", Integer, ForeignKey("menus.id"), nullable=False),
    Column("option_product_id", Integer, ForeignKey("products.id"), nullable=False)
)

from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

menu_products = Table(
    "menu_products",
    Base.metadata,
    Column("menu_id", Integer, ForeignKey("menus.id")),
    Column("product_id", Integer, ForeignKey("products.id"))
)

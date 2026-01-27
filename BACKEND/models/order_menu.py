from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

order_menus = Table(
    "order_menus",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("menu_id", Integer, ForeignKey("menus.id"))
)

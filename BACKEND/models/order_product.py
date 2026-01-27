from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

order_products = Table(
    "order_products",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("product_id", Integer, ForeignKey("products.id"))
)

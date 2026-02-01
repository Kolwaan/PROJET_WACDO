# Import de la base et des tables d'association d'abord
from app.database import Base
from app.models.menu_product import menu_products
from app.models.order_product import order_products
from app.models.order_menu import order_menus

# Import des modèles ensuite
from app.models.product import Product
from app.models.menu import Menu
from app.models.order import Order
from app.models.user import User

__all__ = [
    'Base',
    'menu_products',
    'order_products',
    'order_menus',
    'Product',
    'Menu',
    'Order',
    'User'
]

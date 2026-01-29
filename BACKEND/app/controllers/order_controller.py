from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.product import Product
from app.models.menu import Menu
from app.schemas.order import OrderCreate, OrderUpdate
from app.enums.statut import OrderStatus


def create_order(db: Session, order_data: OrderCreate) -> Order:
    """Créer une nouvelle commande"""
    order = Order(
        chevalet=order_data.chevalet,
        sur_place=order_data.sur_place,
        preparateur_id=order_data.preparateur_id,
        statut=OrderStatus.EN_COURS_PREPARATION
    )
    
    # Associer les produits
    if order_data.product_ids:
        products = db.query(Product).filter(Product.id.in_(order_data.product_ids)).all()
        order.produits = products
    
    # Associer les menus
    if order_data.menu_ids:
        menus = db.query(Menu).filter(Menu.id.in_(order_data.menu_ids)).all()
        order.menus = menus
    
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_all_orders(db: Session) -> list[Order]:
    """Récupérer toutes les commandes"""
    return db.query(Order).all()


def get_order_by_id(db: Session, order_id: int) -> Order | None:
    """Récupérer une commande par ID"""
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders_by_status(db: Session, status: OrderStatus) -> list[Order]:
    """Récupérer les commandes par statut"""
    return db.query(Order).filter(Order.statut == status).all()


def get_orders_by_preparateur(db: Session, preparateur_id: int) -> list[Order]:
    """Récupérer les commandes d'un préparateur"""
    return db.query(Order).filter(Order.preparateur_id == preparateur_id).all()


def get_orders_sur_place(db: Session) -> list[Order]:
    """Récupérer les commandes sur place"""
    return db.query(Order).filter(Order.sur_place == True).all()


def get_orders_a_emporter(db: Session) -> list[Order]:
    """Récupérer les commandes à emporter"""
    return db.query(Order).filter(Order.sur_place == False).all()


def update_order(db: Session, order_id: int, order_data: OrderUpdate) -> Order | None:
    """Mettre à jour une commande"""
    order = get_order_by_id(db, order_id)
    
    if not order:
        return None
    
    # Mettre à jour les champs simples
    for field, value in order_data.dict(exclude_unset=True, exclude={'product_ids', 'menu_ids'}).items():
        setattr(order, field, value)
    
    # Mettre à jour les produits si fournis
    if order_data.product_ids is not None:
        products = db.query(Product).filter(Product.id.in_(order_data.product_ids)).all()
        order.produits = products
    
    # Mettre à jour les menus si fournis
    if order_data.menu_ids is not None:
        menus = db.query(Menu).filter(Menu.id.in_(order_data.menu_ids)).all()
        order.menus = menus
    
    db.commit()
    db.refresh(order)
    return order


def update_order_status(db: Session, order_id: int, new_status: OrderStatus) -> Order | None:
    """Mettre à jour le statut d'une commande"""
    order = get_order_by_id(db, order_id)
    
    if not order:
        return None
    
    order.statut = new_status
    db.commit()
    db.refresh(order)
    return order


def assign_preparateur(db: Session, order_id: int, preparateur_id: int) -> Order | None:
    """Assigner un préparateur à une commande"""
    order = get_order_by_id(db, order_id)
    
    if not order:
        return None
    
    order.preparateur_id = preparateur_id
    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int) -> bool:
    """Supprimer une commande"""
    order = get_order_by_id(db, order_id)
    
    if not order:
        return False
    
    db.delete(order)
    db.commit()
    return True


def get_order_total(db: Session, order_id: int) -> float | None:
    """Calculer le total TTC d'une commande"""
    order = get_order_by_id(db, order_id)
    
    if not order:
        return None
    
    return order.total_ttc()

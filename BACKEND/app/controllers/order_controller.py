from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from app.models.order import Order
from app.models.product import Product
from app.models.menu import Menu
from app.models.user import User
from app.schemas.order import OrderCreate, OrderUpdate
from app.enums.statut import OrderStatus


def _enrich_order_menus_with_options(db: Session, order: Order) -> Order:
    """
    Enrichit les menus d'une commande avec leurs options choisies
    
    Récupère les options (frites, boisson) depuis order_menu_options
    et les ajoute dans menu.produits pour l'affichage
    
    Cela permet au frontend de voir les options dans menu.produits[]
    sans aucune modification du frontend
    """
    for menu in order.menus:
        # Récupérer les options de ce menu pour cette commande
        query = text("""
            SELECT p.* FROM products p
            JOIN order_menu_options omo ON p.id = omo.option_product_id
            WHERE omo.order_id = :order_id AND omo.menu_id = :menu_id
        """)
        
        result = db.execute(query, {"order_id": order.id, "menu_id": menu.id})
        option_ids = [row[0] for row in result]
        
        if option_ids:
            # Récupérer les produits options
            options = db.query(Product).filter(Product.id.in_(option_ids)).all()
            
            # Remplacer la liste des produits du menu par les options choisies
            # Ainsi le frontend verra : "produits": [{id: 15, nom: "Frites"}, {id: 22, nom: "Coca"}]
            menu.produits = list(options)
    
    return order


def create_order(db: Session, order_data: OrderCreate) -> Order:
    """Créer une nouvelle commande"""
    order = Order(
        chevalet=order_data.chevalet,
        sur_place=order_data.sur_place,
        preparateur_id=order_data.preparateur_id,
        statut=OrderStatus.EN_COURS_PREPARATION
    )
    
    # Associer les produits simples
    if order_data.product_ids:
        products = db.query(Product).filter(Product.id.in_(order_data.product_ids)).all()
        order.produits = products
    
    # Gérer les menus avec leurs options (nouvelle approche)
    if order_data.menus_composes:
        menu_ids = [mc.menu_id for mc in order_data.menus_composes]
        menus = db.query(Menu).filter(Menu.id.in_(menu_ids)).all()
        
        # Vérifier que tous les menus existent
        if len(menus) != len(menu_ids):
            raise ValueError("Certains menus n'existent pas")
        
        order.menus = menus
        
        # Sauvegarder la commande pour obtenir un ID
        db.add(order)
        db.flush()
        
        # Insérer les options pour chaque menu
        for menu_compose in order_data.menus_composes:
            # Vérifier que les options (produits) existent
            if menu_compose.product_ids:
                options = db.query(Product).filter(
                    Product.id.in_(menu_compose.product_ids)
                ).all()
                
                if len(options) != len(menu_compose.product_ids):
                    db.rollback()
                    raise ValueError(f"Certaines options du menu {menu_compose.menu_id} n'existent pas")
                
                # Insérer chaque option dans order_menu_options
                for option_id in menu_compose.product_ids:
                    insert_stmt = text("""
                        INSERT INTO order_menu_options (order_id, menu_id, option_product_id)
                        VALUES (:order_id, :menu_id, :option_id)
                    """)
                    db.execute(insert_stmt, {
                        "order_id": order.id,
                        "menu_id": menu_compose.menu_id,
                        "option_id": option_id
                    })
    
    # Support de l'ancienne méthode (menu_ids sans options)
    elif order_data.menu_ids:
        menus = db.query(Menu).filter(Menu.id.in_(order_data.menu_ids)).all()
        order.menus = menus
        db.add(order)
    else:
        db.add(order)
    
    db.commit()
    db.refresh(order)
    
    # Recharger avec toutes les relations
    order = db.query(Order).options(
        joinedload(Order.produits),
        joinedload(Order.menus).joinedload(Menu.produits),
        joinedload(Order.preparateur)
    ).filter(Order.id == order.id).first()
    
    # Enrichir les menus avec leurs options
    return _enrich_order_menus_with_options(db, order)


def get_all_orders(db: Session) -> list[Order]:
    """Récupérer toutes les commandes avec leurs relations"""
    orders = db.query(Order).options(
        joinedload(Order.produits),
        joinedload(Order.menus).joinedload(Menu.produits),
        joinedload(Order.preparateur)
    ).all()
    
    # Enrichir chaque commande
    return [_enrich_order_menus_with_options(db, order) for order in orders]


def get_order_by_id(db: Session, order_id: int) -> Order | None:
    """Récupérer une commande par ID avec toutes ses relations"""
    order = db.query(Order).options(
        joinedload(Order.produits),
        joinedload(Order.menus).joinedload(Menu.produits),
        joinedload(Order.preparateur)
    ).filter(Order.id == order_id).first()
    
    if order:
        return _enrich_order_menus_with_options(db, order)
    return None


def get_orders_by_status(db: Session, status: OrderStatus) -> list[Order]:
    """Récupérer les commandes par statut avec leurs relations"""
    orders = db.query(Order).options(
        joinedload(Order.produits),
        joinedload(Order.menus).joinedload(Menu.produits),
        joinedload(Order.preparateur)
    ).filter(Order.statut == status).all()
    
    return [_enrich_order_menus_with_options(db, order) for order in orders]


def get_orders_by_preparateur(db: Session, preparateur_id: int) -> list[Order]:
    """Récupérer les commandes d'un préparateur avec leurs relations"""
    orders = db.query(Order).options(
        joinedload(Order.produits),
        joinedload(Order.menus).joinedload(Menu.produits),
        joinedload(Order.preparateur)
    ).filter(Order.preparateur_id == preparateur_id).all()
    
    return [_enrich_order_menus_with_options(db, order) for order in orders]


def get_orders_sur_place(db: Session) -> list[Order]:
    """Récupérer les commandes sur place avec leurs relations"""
    orders = db.query(Order).options(
        joinedload(Order.produits),
        joinedload(Order.menus).joinedload(Menu.produits),
        joinedload(Order.preparateur)
    ).filter(Order.sur_place == True).all()
    
    return [_enrich_order_menus_with_options(db, order) for order in orders]


def get_orders_a_emporter(db: Session) -> list[Order]:
    """Récupérer les commandes à emporter avec leurs relations"""
    orders = db.query(Order).options(
        joinedload(Order.produits),
        joinedload(Order.menus).joinedload(Menu.produits),
        joinedload(Order.preparateur)
    ).filter(Order.sur_place == False).all()
    
    return [_enrich_order_menus_with_options(db, order) for order in orders]


def update_order(db: Session, order_id: int, order_data: OrderUpdate) -> Order | None:
    """Mettre à jour une commande"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        return None
    
    # Mettre à jour les champs simples
    for field, value in order_data.model_dump(exclude_unset=True, exclude={'product_ids', 'menu_ids'}).items():
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
    
    # Recharger et enrichir
    return get_order_by_id(db, order_id)


def update_order_status(db: Session, order_id: int, new_status: OrderStatus) -> Order | None:
    """Mettre à jour le statut d'une commande"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        return None
    
    order.statut = new_status
    db.commit()
    db.refresh(order)
    
    # Recharger et enrichir
    return get_order_by_id(db, order_id)


def assign_preparateur(db: Session, order_id: int, preparateur_id: int) -> Order | None:
    """Assigner un préparateur à une commande"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        return None
    
    order.preparateur_id = preparateur_id
    db.commit()
    db.refresh(order)
    
    # Recharger et enrichir
    return get_order_by_id(db, order_id)


def delete_order(db: Session, order_id: int) -> bool:
    """Supprimer une commande"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
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
    
    return order.total_ttc

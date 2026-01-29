from sqlalchemy.orm import Session
from app.models.menu import Menu
from app.models.product import Product
from app.schemas.menu import MenuCreate, MenuUpdate


def create_menu(db: Session, menu_data: MenuCreate) -> Menu:
    """Créer un nouveau menu"""
    menu = Menu(
        nom=menu_data.nom,
        description=menu_data.description,
        prixHT=menu_data.prixHT,
        image=menu_data.image,
        disponibilite=menu_data.disponibilite,
        menu_type=menu_data.menu_type
    )
    
    # Associer les produits si des IDs sont fournis
    if menu_data.product_ids:
        products = db.query(Product).filter(Product.id.in_(menu_data.product_ids)).all()
        menu.produits = products
    
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


def get_all_menus(db: Session) -> list[Menu]:
    """Récupérer tous les menus"""
    return db.query(Menu).all()


def get_menu_by_id(db: Session, menu_id: int) -> Menu | None:
    """Récupérer un menu par ID"""
    return db.query(Menu).filter(Menu.id == menu_id).first()


def get_menus_by_type(db: Session, menu_type: str) -> list[Menu]:
    """Récupérer les menus par type"""
    return db.query(Menu).filter(Menu.menu_type == menu_type).all()


def get_available_menus(db: Session) -> list[Menu]:
    """Récupérer uniquement les menus disponibles"""
    return db.query(Menu).filter(Menu.disponibilite == True).all()


def update_menu(db: Session, menu_id: int, menu_data: MenuUpdate) -> Menu | None:
    """Mettre à jour un menu"""
    menu = get_menu_by_id(db, menu_id)
    
    if not menu:
        return None
    
    # Mettre à jour les champs simples
    for field, value in menu_data.dict(exclude_unset=True, exclude={'product_ids'}).items():
        setattr(menu, field, value)
    
    # Mettre à jour les produits associés si fournis
    if menu_data.product_ids is not None:
        products = db.query(Product).filter(Product.id.in_(menu_data.product_ids)).all()
        menu.produits = products
    
    db.commit()
    db.refresh(menu)
    return menu


def delete_menu(db: Session, menu_id: int) -> bool:
    """Supprimer un menu"""
    menu = get_menu_by_id(db, menu_id)
    
    if not menu:
        return False
    
    db.delete(menu)
    db.commit()
    return True


def toggle_availability(db: Session, menu_id: int) -> Menu | None:
    """Basculer la disponibilité d'un menu"""
    menu = get_menu_by_id(db, menu_id)
    
    if not menu:
        return None
    
    menu.disponibilite = not menu.disponibilite
    db.commit()
    db.refresh(menu)
    return menu


def add_products_to_menu(db: Session, menu_id: int, product_ids: list[int]) -> Menu | None:
    """Ajouter des produits à un menu"""
    menu = get_menu_by_id(db, menu_id)
    
    if not menu:
        return None
    
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    
    # Ajouter les nouveaux produits (sans dupliquer)
    for product in products:
        if product not in menu.produits:
            menu.produits.append(product)
    
    db.commit()
    db.refresh(menu)
    return menu


def remove_products_from_menu(db: Session, menu_id: int, product_ids: list[int]) -> Menu | None:
    """Retirer des produits d'un menu"""
    menu = get_menu_by_id(db, menu_id)
    
    if not menu:
        return None
    
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    
    for product in products:
        if product in menu.produits:
            menu.produits.remove(product)
    
    db.commit()
    db.refresh(menu)
    return menu

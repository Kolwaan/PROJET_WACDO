from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, product_data: ProductCreate) -> Product:
    """Créer un nouveau produit"""
    product = Product(
        nom=product_data.nom,
        description=product_data.description,
        prixHT=product_data.prixHT,
        image=product_data.image,
        options=product_data.options,
        disponibilite=product_data.disponibilite,
        type=product_data.type
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_all_products(db: Session) -> list[Product]:
    """Récupérer tous les produits"""
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int) -> Product | None:
    """Récupérer un produit par ID"""
    return db.query(Product).filter(Product.id == product_id).first()


def get_products_by_type(db: Session, product_type: str) -> list[Product]:
    """Récupérer les produits par type"""
    return db.query(Product).filter(Product.type == product_type).all()


def get_available_products(db: Session) -> list[Product]:
    """Récupérer uniquement les produits disponibles"""
    return db.query(Product).filter(Product.disponibilite == True).all()


def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Product | None:
    """Mettre à jour un produit"""
    product = get_product_by_id(db, product_id)
    
    if not product:
        return None
    
    for field, value in product_data.dict(exclude_unset=True).items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    """Supprimer un produit"""
    product = get_product_by_id(db, product_id)
    
    if not product:
        return False
    
    db.delete(product)
    db.commit()
    return True


def toggle_availability(db: Session, product_id: int) -> Product | None:
    """Basculer la disponibilité d'un produit"""
    product = get_product_by_id(db, product_id)
    
    if not product:
        return None
    
    product.disponibilite = not product.disponibilite
    db.commit()
    db.refresh(product)
    return product

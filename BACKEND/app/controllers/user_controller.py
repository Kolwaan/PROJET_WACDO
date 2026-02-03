from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.enums.role import RoleEnum
from app.utils.hash import hash_password


def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise ValueError("Email déjà utilisé")

    # Hacher le mot de passe avant de le stocker
    hashed_password = hash_password(user_data.password)

    user = User(
        nom=user_data.nom,
        email=user_data.email,
        password=hashed_password,  # ✅ Stockage du mot de passe haché
        role=user_data.role or RoleEnum.AGENT_ACCUEIL
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Récupérer tous les utilisateurs
def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()

# Récupérer un utilisateur par ID
def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

# Supprimer un utilisateur
def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)

    if not user:
        return False

    db.delete(user)
    db.commit()
    return True

# Mettre à jour un utilisateur
def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User | None:
    user = get_user_by_id(db, user_id)

    if not user:
        return None

    # Hacher le nouveau mot de passe si fourni
    update_data = user_data.dict(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["password"] = hash_password(update_data["password"])

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

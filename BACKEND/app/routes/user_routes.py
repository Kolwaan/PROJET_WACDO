from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.controllers.user_controller import (
    create_user,
    get_all_users,
    get_user_by_id,
    delete_user,
    update_user
)
from app.utils.dependencies import get_current_user, require_role
from app.enums.role import RoleEnum


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========================================
# ROUTES ADMINISTRATEUR UNIQUEMENT
# ========================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleEnum.ADMINISTRATEUR))]

)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Inscription d'un nouvel utilisateur.
    Cette route est réservée à l'admin.
    """
    try:
        return create_user(db, user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )



@router.get(
    "/",
    response_model=list[UserResponse],
    dependencies=[Depends(require_role(RoleEnum.ADMINISTRATEUR))],
    summary="Lister tous les utilisateurs (Admin uniquement)"
)
def read_users(db: Session = Depends(get_db)):
    """
    Liste tous les utilisateurs. Accessible uniquement aux administrateurs.
    """
    return get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_role(RoleEnum.ADMINISTRATEUR))],
    summary="Récupérer un utilisateur par ID (Admin uniquement)"
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Récupère un utilisateur spécifique. Accessible uniquement aux administrateurs.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_role(RoleEnum.ADMINISTRATEUR))],
    summary="Modifier un utilisateur (Admin uniquement)"
)
def update_user_route(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour un utilisateur. Accessible uniquement aux administrateurs.
    """
    user = update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(RoleEnum.ADMINISTRATEUR))],
    summary="Supprimer un utilisateur (Admin uniquement)"
)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    """
    Supprime un utilisateur. Accessible uniquement aux administrateurs.
    """
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")


# ========================================
# ROUTES PUBLIQUES
# ========================================


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Récupérer son propre profil"
)
def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les informations du profil de l'utilisateur connecté.
    """
    user = get_user_by_id(db, current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Mettre à jour son propre profil"
)
def update_my_profile(
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Met à jour les informations du profil de l'utilisateur connecté.
    """
    user = update_user(db, current_user["user_id"], user_data)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

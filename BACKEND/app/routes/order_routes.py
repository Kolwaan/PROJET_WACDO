from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.order import (
    OrderCreate, 
    OrderUpdate, 
    OrderResponse, 
    OrderWithDetailsResponse,
    OrderStatusUpdate
)
from app.controllers.order_controller import (
    create_order,
    get_all_orders,
    get_order_by_id,
    get_orders_by_status,
    get_orders_by_preparateur,
    get_orders_sur_place,
    get_orders_a_emporter,
    update_order,
    update_order_status,
    assign_preparateur,
    delete_order,
    get_order_total
)
from app.enums.statut import OrderStatus
from app.enums.role import RoleEnum
from app.utils.dependencies import get_current_user, require_role


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=OrderWithDetailsResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order_route(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle commande (route publique)"""
    try:
        created_order = create_order(db, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return created_order


@router.get("/", response_model=list[OrderWithDetailsResponse],
    dependencies=[Depends(require_role(RoleEnum.ADMINISTRATEUR))]
)
def read_orders(db: Session = Depends(get_db)):
    """Récupérer toutes les commandes avec leurs détails (Administrateur uniquement)"""
    return get_all_orders(db)


@router.get("/status/{order_status}", response_model=list[OrderWithDetailsResponse],
    dependencies=[Depends(require_role(
        RoleEnum.AGENT_ACCUEIL,
        RoleEnum.SUPERVISEUR_DE_PREPARATION,
        RoleEnum.ADMINISTRATEUR
    ))]
)
def read_orders_by_status(order_status: OrderStatus, db: Session = Depends(get_db)):
    """Récupérer les commandes par statut avec leurs détails (accueil, superviseur et admin)"""
    return get_orders_by_status(db, order_status)


@router.get("/preparateur/{preparateur_id}", response_model=list[OrderWithDetailsResponse])
def read_orders_by_preparateur(
    preparateur_id: int,
    current_user: dict = Depends(require_role(
        RoleEnum.AGENT_DE_PREPARATION,
        RoleEnum.SUPERVISEUR_DE_PREPARATION,
        RoleEnum.ADMINISTRATEUR
    )),
    db: Session = Depends(get_db)
):
    """Récupérer les commandes d'un préparateur avec leurs détails"""
    # Vérifier que l'agent de préparation ne consulte que ses propres commandes
    # (sauf si c'est un superviseur ou un admin)
    if current_user["role"] == RoleEnum.AGENT_DE_PREPARATION.value:
        if current_user["user_id"] != preparateur_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous ne pouvez consulter que vos propres commandes"
            )
    
    return get_orders_by_preparateur(db, preparateur_id)


@router.get("/sur-place", response_model=list[OrderWithDetailsResponse],
    dependencies=[Depends(require_role(
        RoleEnum.AGENT_ACCUEIL,
        RoleEnum.SUPERVISEUR_DE_PREPARATION,
        RoleEnum.ADMINISTRATEUR
    ))]
)
def read_orders_sur_place(db: Session = Depends(get_db)):
    """Récupérer les commandes sur place avec leurs détails (Accueil, Superviseur et Admin)"""
    return get_orders_sur_place(db)


@router.get("/a-emporter", response_model=list[OrderWithDetailsResponse],
    dependencies=[Depends(require_role(
        RoleEnum.AGENT_ACCUEIL,
        RoleEnum.SUPERVISEUR_DE_PREPARATION,
        RoleEnum.ADMINISTRATEUR
    ))]
)
def read_orders_a_emporter(db: Session = Depends(get_db)):
    """Récupérer les commandes à emporter avec leurs détails (Accueil, Superviseur et Admin)"""
    return get_orders_a_emporter(db)




@router.get("/{order_id}", response_model=OrderWithDetailsResponse)
def read_order(
    order_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer une commande par ID avec contrôle d'accès selon le rôle"""

    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    user_role = current_user["role"]

    # Si c'est un agent de préparation → accès uniquement à ses commandes
    if user_role == RoleEnum.AGENT_DE_PREPARATION.value:
        if order.preparateur_id != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous ne pouvez consulter que vos propres commandes"
            )

    # Les autres rôles autorisés (accueil, superviseur, admin) ont accès libre
    return order


@router.get("/{order_id}/total",
    dependencies=[Depends(get_current_user)]
)
def get_total(order_id: int, db: Session = Depends(get_db)):
    """Obtenir le total TTC d'une commande (Authentification requise)"""
    total = get_order_total(db, order_id)
    if total is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return {"order_id": order_id, "total_ttc": total}


@router.put("/{order_id}", response_model=OrderWithDetailsResponse,
    dependencies=[Depends(require_role(RoleEnum.ADMINISTRATEUR))]
)
def update_order_route(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une commande (Administrateur uniquement)"""
    order = update_order(db, order_id, order_data)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order




@router.patch("/{order_id}/status", response_model=OrderWithDetailsResponse)
def update_status_route(
    order_id: int,
    status_data: OrderStatusUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour le statut d'une commande (Permissions selon rôle + attribution)"""

    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    target_status = status_data.statut
    user_role = current_user["role"]

    # Si agent de préparation → vérifier que la commande lui appartient
    if user_role == RoleEnum.AGENT_DE_PREPARATION.value:
        if order.preparateur_id != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous ne pouvez modifier que vos propres commandes"
            )

    # Vérification des permissions selon le statut cible
    if target_status == OrderStatus.LIVREE:
        # Seuls l'accueil, le superviseur et l'admin peuvent livrer
        if user_role not in [
            RoleEnum.AGENT_ACCUEIL.value,
            RoleEnum.SUPERVISEUR_DE_PREPARATION.value,
            RoleEnum.ADMINISTRATEUR.value
        ]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seul un agent d'accueil peut marquer une commande comme livrée"
            )

    elif target_status == OrderStatus.PREPAREE:
        # Le préparateur (sur ses commandes), le superviseur et l'admin peuvent marquer PREPAREE
        if user_role not in [
            RoleEnum.AGENT_DE_PREPARATION.value,
            RoleEnum.SUPERVISEUR_DE_PREPARATION.value,
            RoleEnum.ADMINISTRATEUR.value
        ]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seul un agent de préparation peut marquer une commande comme préparée"
            )

    elif target_status == OrderStatus.EN_COURS_PREPARATION:
        # Seuls le superviseur et l'admin peuvent (re)mettre EN_COURS
        if user_role not in [
            RoleEnum.SUPERVISEUR_DE_PREPARATION.value,
            RoleEnum.ADMINISTRATEUR.value
        ]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seul un superviseur peut remettre une commande en cours de préparation"
            )

    return update_order_status(db, order_id, target_status)



@router.patch("/{order_id}/assign/{preparateur_id}", response_model=OrderWithDetailsResponse,
    dependencies=[Depends(require_role(
        RoleEnum.SUPERVISEUR_DE_PREPARATION,
        RoleEnum.ADMINISTRATEUR
        ))]
)
def assign_preparateur_route(
    order_id: int,
    preparateur_id: int,
    db: Session = Depends(get_db)
):
    """Assigner un préparateur à une commande (Superviseur et Admin)"""
    order = assign_preparateur(db, order_id, preparateur_id)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order




@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(RoleEnum.ADMINISTRATEUR))]
)
def delete_order_route(order_id: int, db: Session = Depends(get_db)):
    """Supprimer une commande (Administrateur uniquement)"""
    success = delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

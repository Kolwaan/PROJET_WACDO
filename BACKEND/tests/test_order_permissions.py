# Vérifie les restrictions d'accès selon les rôles.

import pytest
from fastapi import status


class TestOrderPermissions:
    """Tests de sécurisation des routes de commandes."""
    
    # ==========================================
    # Tests de la route POST /orders/ (Création)
    # ==========================================
    
    def test_accueil_can_create_order(self, client, accueil_token, auth_headers, sample_order_data):
        # Un agent d'accueil peut créer une commande.
        response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["numero"] == "CMD001"
    
    def test_preparateur_cannot_create_order(self, client, preparateur_token, auth_headers, sample_order_data):
        # Un préparateur ne peut pas créer de commande.
        response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Accès refusé" in response.json()["detail"]
    
    def test_superviseur_cannot_create_order(self, client, superviseur_token, auth_headers, sample_order_data):
        # """❌ Un superviseur ne peut pas créer de commande."""
        response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_admin_cannot_create_order(self, client, admin_token, auth_headers, sample_order_data):
        # """❌ Même un admin ne peut pas créer de commande (réservé à l'accueil)."""
        response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_unauthenticated_cannot_create_order(self, client, sample_order_data):
        # """❌ Sans authentification, impossible de créer une commande."""
        response = client.post("/orders/", json=sample_order_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # ==========================================
    # Tests de la route GET /orders/ (Liste complète)
    # ==========================================
    
    def test_admin_can_list_all_orders(self, client, admin_token, auth_headers):
        # """✅ Un administrateur peut lister toutes les commandes."""
        response = client.get(
            "/orders/",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
    
    def test_preparateur_cannot_list_all_orders(self, client, preparateur_token, auth_headers):
        # """❌ Un préparateur ne peut pas lister toutes les commandes."""
        response = client.get(
            "/orders/",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_accueil_cannot_list_all_orders(self, client, accueil_token, auth_headers):
        # """❌ Un agent d'accueil ne peut pas lister toutes les commandes."""
        response = client.get(
            "/orders/",
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route GET /orders/status/{status}
    # ==========================================
    
    def test_preparateur_can_view_orders_by_status(self, client, preparateur_token, auth_headers):
        # """✅ Un préparateur peut voir les commandes par statut."""
        response = client.get(
            "/orders/status/EN_COURS_PREPARATION",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_superviseur_can_view_orders_by_status(self, client, superviseur_token, auth_headers):
        """✅ Un superviseur peut voir les commandes par statut."""
        response = client.get(
            "/orders/status/PREPAREE",
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_accueil_can_view_orders_by_status(self, client, accueil_token, auth_headers):
        """✅ Un agent d'accueil peut voir les commandes par statut."""
        response = client.get(
            "/orders/status/PREPAREE",
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_admin_cannot_view_orders_by_status(self, client, admin_token, auth_headers):
        """❌ Un admin ne peut pas utiliser cette route (non autorisé)."""
        response = client.get(
            "/orders/status/EN_COURS_PREPARATION",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route GET /orders/preparateur/{id}
    # ==========================================
    
    def test_preparateur_can_view_own_orders(self, client, preparateur_token, auth_headers):
        """✅ Un préparateur peut voir ses propres commandes."""
        # L'user_id du preparateur_token est 3
        response = client.get(
            "/orders/preparateur/3",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_preparateur_cannot_view_other_orders(self, client, preparateur_token, auth_headers):
        """❌ Un préparateur ne peut pas voir les commandes d'un autre préparateur."""
        # L'user_id du preparateur_token est 3, on essaie d'accéder au préparateur 5
        response = client.get(
            "/orders/preparateur/5",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "vos propres commandes" in response.json()["detail"]
    
    def test_superviseur_can_view_any_preparateur_orders(self, client, superviseur_token, auth_headers):
        """✅ Un superviseur peut voir les commandes de n'importe quel préparateur."""
        response = client.get(
            "/orders/preparateur/3",
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_accueil_cannot_view_preparateur_orders(self, client, accueil_token, auth_headers):
        """❌ Un agent d'accueil ne peut pas voir les commandes des préparateurs."""
        response = client.get(
            "/orders/preparateur/3",
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route GET /orders/sur-place et /a-emporter
    # ==========================================
    
    def test_accueil_can_view_sur_place_orders(self, client, accueil_token, auth_headers):
        """✅ Un agent d'accueil peut voir les commandes sur place."""
        response = client.get(
            "/orders/sur-place",
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_superviseur_can_view_sur_place_orders(self, client, superviseur_token, auth_headers):
        """✅ Un superviseur peut voir les commandes sur place."""
        response = client.get(
            "/orders/sur-place",
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_preparateur_cannot_view_sur_place_orders(self, client, preparateur_token, auth_headers):
        """❌ Un préparateur ne peut pas voir les commandes sur place."""
        response = client.get(
            "/orders/sur-place",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route GET /orders/{order_id}
    # ==========================================
    
    def test_authenticated_user_can_view_order(self, client, accueil_token, preparateur_token, auth_headers, sample_order_data):
        """✅ N'importe quel utilisateur authentifié peut voir une commande."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Consulter avec un préparateur
        response = client.get(
            f"/orders/{order_id}",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_unauthenticated_cannot_view_order(self, client):
        """❌ Sans authentification, impossible de voir une commande."""
        response = client.get("/orders/1")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # ==========================================
    # Tests de la route PATCH /orders/{id}/status
    # ==========================================
    
    def test_preparateur_can_change_to_en_preparation(self, client, accueil_token, preparateur_token, auth_headers, sample_order_data):
        """✅ Un préparateur peut mettre une commande EN_COURS_PREPARATION."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Changer le statut
        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "EN_COURS_PREPARATION"},
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_preparateur_can_change_to_preparee(self, client, accueil_token, preparateur_token, auth_headers, sample_order_data):
        """✅ Un préparateur peut mettre une commande PREPAREE."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Changer le statut
        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "PREPAREE"},
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_accueil_can_change_to_livree(self, client, accueil_token, auth_headers, sample_order_data):
        """✅ Un agent d'accueil peut livrer une commande (statut LIVREE)."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Livrer la commande
        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "LIVREE"},
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_preparateur_cannot_change_to_livree(self, client, accueil_token, preparateur_token, auth_headers, sample_order_data):
        """❌ Un préparateur ne peut pas livrer une commande."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Tenter de livrer
        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "LIVREE"},
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "agent d'accueil" in response.json()["detail"]
    
    def test_accueil_cannot_change_to_en_preparation(self, client, accueil_token, auth_headers, sample_order_data):
        """❌ Un agent d'accueil ne peut pas changer vers EN_COURS_PREPARATION."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Tenter de changer le statut
        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "EN_COURS_PREPARATION"},
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "agent de préparation" in response.json()["detail"]
    
    # ==========================================
    # Tests de la route PATCH /orders/{id}/assign/{preparateur_id}
    # ==========================================
    
    def test_superviseur_can_assign_preparateur(self, client, accueil_token, superviseur_token, auth_headers, sample_order_data):
        """✅ Un superviseur peut assigner un préparateur."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Assigner un préparateur
        response = client.patch(
            f"/orders/{order_id}/assign/3",
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_preparateur_cannot_assign(self, client, accueil_token, preparateur_token, auth_headers, sample_order_data):
        """❌ Un agent de préparation ne peut pas assigner."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Tenter d'assigner
        response = client.patch(
            f"/orders/{order_id}/assign/3",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_accueil_cannot_assign(self, client, accueil_token, auth_headers, sample_order_data):
        """❌ Un agent d'accueil ne peut pas assigner."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Tenter d'assigner
        response = client.patch(
            f"/orders/{order_id}/assign/3",
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route PUT /orders/{order_id} (Modification complète)
    # ==========================================
    
    def test_admin_can_update_order(self, client, accueil_token, admin_token, auth_headers, sample_order_data):
        """✅ Un administrateur peut modifier une commande."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Modifier
        update_data = {"numero": "CMD002"}
        response = client.put(
            f"/orders/{order_id}",
            json=update_data,
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_preparateur_cannot_update_order(self, client, accueil_token, preparateur_token, auth_headers, sample_order_data):
        """❌ Un préparateur ne peut pas modifier une commande."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Tenter de modifier
        update_data = {"numero": "HACKED"}
        response = client.put(
            f"/orders/{order_id}",
            json=update_data,
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route DELETE /orders/{order_id}
    # ==========================================
    
    def test_admin_can_delete_order(self, client, accueil_token, admin_token, auth_headers, sample_order_data):
        """✅ Un administrateur peut supprimer une commande."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Supprimer
        response = client.delete(
            f"/orders/{order_id}",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_accueil_cannot_delete_order(self, client, accueil_token, auth_headers, sample_order_data):
        """❌ Un agent d'accueil ne peut pas supprimer une commande."""
        # Créer une commande
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]
        
        # Tenter de supprimer
        response = client.delete(
            f"/orders/{order_id}",
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

# Tests de sécurisation des commandes

import pytest
from fastapi import status


class TestOrderPermissions:

    # ==========================================
    # POST /orders/ - Création (route publique)
    # ==========================================

    def test_create_order_without_auth(self, client, sample_order_data):
        """Une commande peut être créée sans authentification (route publique)"""
        response = client.post("/orders/", json=sample_order_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()
        assert "menus" in response.json()

    def test_create_order_with_menu_and_options(self, client):
        """Une commande peut être créée avec un menu et ses options"""
        order_data = {
            "chevalet": 42,
            "sur_place": True,
            "menu_ids": [
                {
                    "menu_id": 1,
                    "product_ids": [1, 2]  # Frites + Boisson
                }
            ]
        }
        response = client.post("/orders/", json=order_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Vérifier que les options apparaissent dans le menu
        order = response.json()
        assert len(order["menus"]) == 1
        # Les options doivent apparaître dans menu.produits
        # (si les produits 1 et 2 existent dans la DB de test)

    def test_create_order_with_simple_products(self, client):
        """Une commande peut contenir des produits simples"""
        order_data = {
            "chevalet": 10,
            "sur_place": False,
            "product_ids": [1, 2]
        }
        response = client.post("/orders/", json=order_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_order_mixed(self, client):
        """Une commande peut contenir à la fois des menus et des produits"""
        order_data = {
            "chevalet": 15,
            "sur_place": True,
            "product_ids": [1],
            "menu_ids": [
                {
                    "menu_id": 1,
                    "product_ids": [2, 3]
                }
            ]
        }
        response = client.post("/orders/", json=order_data)
        assert response.status_code == status.HTTP_201_CREATED

    # ==========================================
    # GET /orders/ - Liste (Admin uniquement)
    # ==========================================

    def test_admin_can_list_all_orders(self, client, admin_token, auth_headers):
        """Un admin peut lister toutes les commandes"""
        response = client.get("/orders/", headers=auth_headers(admin_token))
        assert response.status_code == status.HTTP_200_OK

    def test_non_admin_cannot_list_all_orders(self, client, preparateur_token, auth_headers):
        """Un non-admin ne peut pas lister toutes les commandes"""
        response = client.get("/orders/", headers=auth_headers(preparateur_token))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # GET /orders/{id} - Détails (Authentifié)
    # ==========================================

    def test_authenticated_user_can_view_order(self, client, preparateur_token, auth_headers, sample_order_data):
        """Un utilisateur authentifié peut voir une commande qui lui est attribuée"""
        # Créer une commande assignée au préparateur (user_id=3)
        order_data = {**sample_order_data, "preparateur_id": 3}
        create_resp = client.post("/orders/", json=order_data)
        order_id = create_resp.json()["id"]

        # La consulter
        response = client.get(f"/orders/{order_id}", headers=auth_headers(preparateur_token))
        assert response.status_code == status.HTTP_200_OK    
        
    def test_unauthenticated_cannot_view_order(self, client, sample_order_data):
        """Un utilisateur non authentifié ne peut pas voir une commande"""
        # Créer une commande
        create_resp = client.post("/orders/", json=sample_order_data)
        order_id = create_resp.json()["id"]
        
        # Essayer de la consulter sans auth
        response = client.get(f"/orders/{order_id}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        
    def test_preparateur_cannot_view_other_order(self, client, preparateur_token, auth_headers, sample_order_data):
        """Un préparateur ne peut pas voir une commande qui ne lui appartient pas"""
        # Créer une commande assignée à un AUTRE préparateur (user_id=1, pas 3)
        order_data = {**sample_order_data, "preparateur_id": 1}
        create_resp = client.post("/orders/", json=order_data)
        order_id = create_resp.json()["id"]

        response = client.get(f"/orders/{order_id}", headers=auth_headers(preparateur_token))
        assert response.status_code == status.HTTP_403_FORBIDDEN    

        # ==========================================
        # PATCH /orders/{id}/status - Changement de statut
        # ==========================================

    def test_preparateur_can_change_status(self, client, preparateur_token, auth_headers, sample_order_data):
        """Un préparateur peut changer le statut d'une commande qui lui est attribuée"""
        # Créer une commande assignée au préparateur (user_id=3)
        order_data = {**sample_order_data, "preparateur_id": 3}
        create_resp = client.post("/orders/", json=order_data)
        order_id = create_resp.json()["id"]

        # Changer le statut
        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "PREPAREE"},
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_200_OK
        
        
    def test_preparateur_cannot_modify_other_order(self, client, preparateur_token, auth_headers, sample_order_data):
        """Un préparateur ne peut pas modifier le statut d'une commande qui ne lui appartient pas"""
        # Créer une commande assignée à un AUTRE préparateur (user_id=1, pas 3)
        order_data = {**sample_order_data, "preparateur_id": 1}
        create_resp = client.post("/orders/", json=order_data)
        order_id = create_resp.json()["id"]

        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "PREPAREE"},
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN        
        
        
    def test_accueil_can_deliver_order(self, client, accueil_token, auth_headers, sample_order_data):
        """Un agent d'accueil peut livrer une commande"""
        # Créer une commande
        create_resp = client.post("/orders/", json=sample_order_data)
        order_id = create_resp.json()["id"]
        
        # Livrer
        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "LIVREE"},
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_200_OK
        
        
        
    def test_preparateur_can_set_preparee(self, client, preparateur_token, auth_headers, sample_order_data):
        """Un préparateur peut marquer sa commande comme PREPAREE"""
        order_data = {**sample_order_data, "preparateur_id": 3}
        order_id = client.post("/orders/", json=order_data).json()["id"]

        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "PREPAREE"},
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["statut"] == "PREPAREE"

    def test_preparateur_cannot_set_livree(self, client, preparateur_token, auth_headers, sample_order_data):
        """Un préparateur ne peut pas marquer une commande comme LIVREE"""
        order_data = {**sample_order_data, "preparateur_id": 3}
        order_id = client.post("/orders/", json=order_data).json()["id"]

        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "LIVREE"},
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_preparateur_cannot_set_en_cours(self, client, preparateur_token, auth_headers, sample_order_data):
        """Un préparateur ne peut pas remettre une commande EN_COURS_PREPARATION"""
        order_data = {**sample_order_data, "preparateur_id": 3}
        order_id = client.post("/orders/", json=order_data).json()["id"]

        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "EN_COURS_PREPARATION"},
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_accueil_can_set_livree(self, client, accueil_token, auth_headers, sample_order_data):
        """Un agent d'accueil peut marquer une commande comme LIVREE"""
        order_id = client.post("/orders/", json=sample_order_data).json()["id"]

        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "LIVREE"},
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_200_OK

    def test_accueil_cannot_set_preparee(self, client, accueil_token, auth_headers, sample_order_data):
        """Un agent d'accueil ne peut pas marquer une commande comme PREPAREE"""
        order_id = client.post("/orders/", json=sample_order_data).json()["id"]

        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "PREPAREE"},
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_superviseur_can_set_any_status(self, client, superviseur_token, auth_headers, sample_order_data):
        """Un superviseur peut mettre n'importe quel statut"""
        order_id = client.post("/orders/", json=sample_order_data).json()["id"]

        for statut_cible in ["PREPAREE", "LIVREE", "EN_COURS_PREPARATION"]:
            response = client.patch(
                f"/orders/{order_id}/status",
                json={"statut": statut_cible},
                headers=auth_headers(superviseur_token)
            )
            assert response.status_code == status.HTTP_200_OK

    def test_admin_can_set_any_status(self, client, admin_token, auth_headers, sample_order_data):
        """Un admin peut mettre n'importe quel statut"""
        order_id = client.post("/orders/", json=sample_order_data).json()["id"]

        for statut_cible in ["PREPAREE", "LIVREE", "EN_COURS_PREPARATION"]:
            response = client.patch(
                f"/orders/{order_id}/status",
                json={"statut": statut_cible},
                headers=auth_headers(admin_token)
            )
            assert response.status_code == status.HTTP_200_OK

    # ==========================================
    # DELETE /orders/{id} - Suppression (Admin)
    # ==========================================

    def test_admin_can_delete_order(self, client, admin_token, auth_headers, sample_order_data):
        """Un admin peut supprimer une commande"""
        # Créer une commande
        create_resp = client.post("/orders/", json=sample_order_data)
        order_id = create_resp.json()["id"]
        
        # Supprimer
        response = client.delete(f"/orders/{order_id}", headers=auth_headers(admin_token))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_non_admin_cannot_delete_order(self, client, preparateur_token, auth_headers, sample_order_data):
        """Un non-admin ne peut pas supprimer une commande"""
        # Créer une commande
        create_resp = client.post("/orders/", json=sample_order_data)
        order_id = create_resp.json()["id"]
        
        # Essayer de supprimer
        response = client.delete(f"/orders/{order_id}", headers=auth_headers(preparateur_token))
        assert response.status_code == status.HTTP_403_FORBIDDEN
# Tests de sécurisation des commandes

import pytest
from fastapi import status


    # Tests pour les routes de commandes
class TestOrderPermissions:

    # ==========================================
    # Création de commande POST /orders/
    # ==========================================

    # Un agent d'accueil peut créer une commande
    def test_accueil_can_create_order(self, client, accueil_token, auth_headers, sample_order_data):
        response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_201_CREATED

    # Un utilisateur non accueil ne peut pas créer de commande
    def test_non_accueil_cannot_create_order(self, client, preparateur_token, auth_headers, sample_order_data):
        response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # Un utilisateur non authentifié ne peut pas créer de commande
    def test_unauthenticated_cannot_create_order(self, client, sample_order_data):
        response = client.post("/orders/", json=sample_order_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # ==========================================
    # Liste complète des commandes GET /orders/
    # ==========================================

    # Un administrateur peut lister toutes les commandes
    def test_admin_can_list_all_orders(self, client, admin_token, auth_headers):
        response = client.get(
            "/orders/",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK

    # Un non-admin ne peut pas lister toutes les commandes
    def test_non_admin_cannot_list_all_orders(self, client, preparateur_token, auth_headers):
        response = client.get(
            "/orders/",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Voir commandes par statut GET /orders/status/{status}
    # ==========================================

    # Préparateur, superviseur et accueil peuvent voir certaines commandes par statut
    def test_roles_can_view_orders_by_status(self, client, preparateur_token, superviseur_token, accueil_token, auth_headers):
        for token in [preparateur_token, superviseur_token, accueil_token]:
            response = client.get(
                "/orders/status/EN_COURS_PREPARATION",
                headers=auth_headers(token)
            )
            assert response.status_code == status.HTTP_200_OK

    # Un admin ne peut pas accéder aux commandes par statut
    def test_admin_cannot_view_orders_by_status(self, client, admin_token, auth_headers):
        response = client.get(
            "/orders/status/EN_COURS_PREPARATION",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Voir commandes d'un préparateur GET /orders/preparateur/{id}
    # ==========================================

    # Un préparateur peut voir ses propres commandes
    def test_preparateur_can_view_own_orders(self, client, preparateur_token, auth_headers):
        response = client.get(
            "/orders/preparateur/3",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_200_OK

    # Un préparateur ne peut pas voir les commandes d'un autre préparateur
    def test_preparateur_cannot_view_other_orders(self, client, preparateur_token, auth_headers):
        response = client.get(
            "/orders/preparateur/5",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Modifier le statut PATCH /orders/{id}/status
    # ==========================================

    # Préparateur peut changer les statuts autorisés
    def test_preparateur_can_change_status(self, client, accueil_token, preparateur_token, auth_headers, sample_order_data):
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]

        for statut in ["EN_COURS_PREPARATION", "PREPAREE"]:
            response = client.patch(
                f"/orders/{order_id}/status",
                json={"statut": statut},
                headers=auth_headers(preparateur_token)
            )
            assert response.status_code == status.HTTP_200_OK

    # Seul un préparateur peut mettre EN_COURS_PREPARATION
    def test_non_preparateur_cannot_change_to_en_preparation(self, client, accueil_token, auth_headers, sample_order_data):
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]

        response = client.patch(
            f"/orders/{order_id}/status",
            json={"statut": "EN_COURS_PREPARATION"},
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Assigner un préparateur PATCH /orders/{id}/assign/{preparateur_id}
    # ==========================================

    # Un superviseur peut assigner un préparateur
    def test_superviseur_can_assign_preparateur(self, client, accueil_token, superviseur_token, auth_headers, sample_order_data):
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]

        response = client.patch(
            f"/orders/{order_id}/assign/3",
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_200_OK

    # Seul un superviseur peut assigner un préparateur
    def test_non_superviseur_cannot_assign(self, client, accueil_token, preparateur_token, auth_headers, sample_order_data):
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]

        response = client.patch(
            f"/orders/{order_id}/assign/3",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Modification complète PUT /orders/{order_id}
    # ==========================================

    # Un admin peut modifier une commande
    def test_admin_can_update_order(self, client, accueil_token, admin_token, auth_headers, sample_order_data):
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]

        response = client.put(
            f"/orders/{order_id}",
            json={"numero": "CMD002"},
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK

    # Un non-admin ne peut pas modifier une commande
    def test_non_admin_cannot_update_order(self, client, accueil_token, preparateur_token, auth_headers, sample_order_data):
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]

        response = client.put(
            f"/orders/{order_id}",
            json={"numero": "HACKED"},
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Suppression DELETE /orders/{order_id}
    # ==========================================

    # Un administrateur peut supprimer une commande
    def test_admin_can_delete_order(self, client, accueil_token, admin_token, auth_headers, sample_order_data):
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]

        response = client.delete(
            f"/orders/{order_id}",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    # Un non-admin ne peut pas supprimer une commande
    def test_non_admin_cannot_delete_order(self, client, accueil_token, preparateur_token, auth_headers, sample_order_data):
        create_response = client.post(
            "/orders/",
            json=sample_order_data,
            headers=auth_headers(accueil_token)
        )
        order_id = create_response.json()["id"]

        response = client.delete(
            f"/orders/{order_id}",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

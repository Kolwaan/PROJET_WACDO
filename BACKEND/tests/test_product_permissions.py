# Tests de sécurisation des produits

import pytest
from fastapi import status


class TestProductPermissions:
    # Tests pour les routes produits

    # ==========================================
    # Création de produit POST /products/
    # ==========================================

    # Un administrateur peut créer un produit
    def test_admin_can_create_product(self, client, admin_token, auth_headers, sample_product_data):
        response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["nom"] == "Big Mac"

    # Un non-admin ne peut pas créer un produit
    def test_non_admin_cannot_create_product(self, client, preparateur_token, auth_headers, sample_product_data):
        response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_create_product(self, client, sample_product_data):
        response = client.post("/products/", json=sample_product_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # ==========================================
    # Liste des produits GET /products/
    # ==========================================

    # La liste des produits est publique
    def test_anyone_can_list_products(self, client):
        response = client.get("/products/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    # Un utilisateur authentifié peut lister les produits
    def test_authenticated_user_can_list_products(self, client, preparateur_token, auth_headers):
        response = client.get(
            "/products/",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_200_OK

    # ==========================================
    # Produits disponibles GET /products/available
    # ==========================================

    # La liste des produits disponibles est publique
    def test_anyone_can_list_available_products(self, client):
        response = client.get("/products/available")
        assert response.status_code == status.HTTP_200_OK

    # ==========================================
    # Consulter un produit GET /products/{product_id}
    # ==========================================

    # Consulter un produit est public
    def test_anyone_can_view_product(self, client, admin_token, auth_headers, sample_product_data):
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        response = client.get(f"/products/{product_id}")
        assert response.status_code == status.HTTP_200_OK

    # ==========================================
    # Modifier un produit PUT /products/{product_id}
    # ==========================================

    # Un administrateur peut modifier un produit
    def test_admin_can_update_product(self, client, admin_token, auth_headers, sample_product_data):
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        response = client.put(
            f"/products/{product_id}",
            json={"nom": "Big Mac Updated"},
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["nom"] == "Big Mac Updated"

    # Un non-admin ne peut pas modifier un produit
    def test_non_admin_cannot_update_product(self, client, admin_token, preparateur_token, auth_headers, sample_product_data):
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        response = client.put(
            f"/products/{product_id}",
            json={"nom": "Hacked"},
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Basculer disponibilité PATCH /products/{id}/toggle-availability
    # ==========================================

    # Un administrateur peut basculer la disponibilité
    def test_admin_can_toggle_availability(self, client, admin_token, auth_headers, sample_product_data):
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        response = client.patch(
            f"/products/{product_id}/toggle-availability",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK

    # Un non-admin ne peut pas basculer la disponibilité
    def test_non_admin_cannot_toggle_availability(self, client, admin_token, preparateur_token, auth_headers, sample_product_data):
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        response = client.patch(
            f"/products/{product_id}/toggle-availability",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Supprimer un produit DELETE /products/{product_id}
    # ==========================================

    # Un administrateur peut supprimer un produit
    def test_admin_can_delete_product(self, client, admin_token, auth_headers, sample_product_data):
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        response = client.delete(
            f"/products/{product_id}",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    # Un non-admin ne peut pas supprimer un produit
    def test_non_admin_cannot_delete_product(self, client, admin_token, preparateur_token, auth_headers, sample_product_data):
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        response = client.delete(
            f"/products/{product_id}",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

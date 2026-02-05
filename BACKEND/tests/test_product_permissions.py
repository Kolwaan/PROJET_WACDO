# Vérifie que seuls les administrateurs peuvent gérer les produits.

import pytest
from fastapi import status


class TestProductPermissions:
    """Tests de sécurisation des routes produits."""
    
    # ==========================================
    # Tests de la route POST /products/ (Création)
    # ==========================================
    
    def test_admin_can_create_product(self, client, admin_token, auth_headers, sample_product_data):
        """✅ Un administrateur peut créer un produit."""
        response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["nom"] == "Big Mac"
    
    def test_preparateur_cannot_create_product(self, client, preparateur_token, auth_headers, sample_product_data):
        """❌ Un préparateur ne peut pas créer de produit."""
        response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_superviseur_cannot_create_product(self, client, superviseur_token, auth_headers, sample_product_data):
        """❌ Un superviseur ne peut pas créer de produit."""
        response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_accueil_cannot_create_product(self, client, accueil_token, auth_headers, sample_product_data):
        """❌ Un agent d'accueil ne peut pas créer de produit."""
        response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_unauthenticated_cannot_create_product(self, client, sample_product_data):
        """❌ Sans authentification, impossible de créer un produit."""
        response = client.post("/products/", json=sample_product_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # ==========================================
    # Tests de la route GET /products/ (Liste)
    # ==========================================
    
    def test_anyone_can_list_products(self, client):
        """✅ La liste des produits est accessible sans authentification."""
        response = client.get("/products/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
    
    def test_authenticated_user_can_list_products(self, client, preparateur_token, auth_headers):
        """✅ Un utilisateur authentifié peut lister les produits."""
        response = client.get(
            "/products/",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    # ==========================================
    # Tests de la route GET /products/available
    # ==========================================
    
    def test_anyone_can_list_available_products(self, client):
        """✅ La liste des produits disponibles est publique."""
        response = client.get("/products/available")
        assert response.status_code == status.HTTP_200_OK
    
    # ==========================================
    # Tests de la route GET /products/{product_id}
    # ==========================================
    
    def test_anyone_can_view_product(self, client, admin_token, auth_headers, sample_product_data):
        """✅ Consulter un produit est public."""
        # Créer un produit
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        
        # Consulter sans authentification
        response = client.get(f"/products/{product_id}")
        assert response.status_code == status.HTTP_200_OK
    
    # ==========================================
    # Tests de la route PUT /products/{product_id}
    # ==========================================
    
    def test_admin_can_update_product(self, client, admin_token, auth_headers, sample_product_data):
        """✅ Un administrateur peut modifier un produit."""
        # Créer un produit
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        
        # Modifier le produit
        update_data = {"nom": "Big Mac Updated"}
        response = client.put(
            f"/products/{product_id}",
            json=update_data,
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["nom"] == "Big Mac Updated"
    
    def test_preparateur_cannot_update_product(self, client, admin_token, preparateur_token, auth_headers, sample_product_data):
        """❌ Un préparateur ne peut pas modifier un produit."""
        # Créer un produit
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        
        # Tenter de modifier
        update_data = {"nom": "Hacked"}
        response = client.put(
            f"/products/{product_id}",
            json=update_data,
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_accueil_cannot_update_product(self, client, admin_token, accueil_token, auth_headers, sample_product_data):
        """❌ Un agent d'accueil ne peut pas modifier un produit."""
        # Créer un produit
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        
        # Tenter de modifier
        update_data = {"nom": "Hacked"}
        response = client.put(
            f"/products/{product_id}",
            json=update_data,
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route PATCH /products/{id}/toggle-availability
    # ==========================================
    
    def test_admin_can_toggle_availability(self, client, admin_token, auth_headers, sample_product_data):
        """✅ Un administrateur peut basculer la disponibilité."""
        # Créer un produit
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        
        # Basculer la disponibilité
        response = client.patch(
            f"/products/{product_id}/toggle-availability",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_superviseur_can_toggle_availability(self, client, admin_token, superviseur_token, auth_headers, sample_product_data):
        """✅ Un superviseur peut basculer la disponibilité."""
        # Créer un produit
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        
        # Basculer la disponibilité
        response = client.patch(
            f"/products/{product_id}/toggle-availability",
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_preparateur_cannot_toggle_availability(self, client, admin_token, preparateur_token, auth_headers, sample_product_data):
        """❌ Un préparateur ne peut pas basculer la disponibilité."""
        # Créer un produit
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        
        # Tenter de basculer
        response = client.patch(
            f"/products/{product_id}/toggle-availability",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_accueil_cannot_toggle_availability(self, client, admin_token, accueil_token, auth_headers, sample_product_data):
        """❌ Un agent d'accueil ne peut pas basculer la disponibilité."""
        # Créer un produit
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        
        # Tenter de basculer
        response = client.patch(
            f"/products/{product_id}/toggle-availability",
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route DELETE /products/{product_id}
    # ==========================================
    
    def test_admin_can_delete_product(self, client, admin_token, auth_headers, sample_product_data):
        """✅ Un administrateur peut supprimer un produit."""
        # Créer un produit
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        
        # Supprimer le produit
        response = client.delete(
            f"/products/{product_id}",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_superviseur_cannot_delete_product(self, client, admin_token, superviseur_token, auth_headers, sample_product_data):
        """❌ Un superviseur ne peut pas supprimer un produit."""
        # Créer un produit
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        
        # Tenter de supprimer
        response = client.delete(
            f"/products/{product_id}",
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_preparateur_cannot_delete_product(self, client, admin_token, preparateur_token, auth_headers, sample_product_data):
        """❌ Un préparateur ne peut pas supprimer un produit."""
        # Créer un produit
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        
        # Tenter de supprimer
        response = client.delete(
            f"/products/{product_id}",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_accueil_cannot_delete_product(self, client, admin_token, accueil_token, auth_headers, sample_product_data):
        """❌ Un agent d'accueil ne peut pas supprimer un produit."""
        # Créer un produit
        create_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = create_response.json()["id"]
        
        # Tenter de supprimer
        response = client.delete(
            f"/products/{product_id}",
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

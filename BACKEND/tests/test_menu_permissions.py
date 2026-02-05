# Vérifie que seuls les administrateurs peuvent gérer les menus.

import pytest
from fastapi import status


class TestMenuPermissions:
    """Tests de sécurisation des routes menus."""
    
    # ==========================================
    # Tests de la route POST /menus/ (Création)
    # ==========================================
    
    def test_admin_can_create_menu(self, client, admin_token, auth_headers, sample_menu_data):
        """✅ Un administrateur peut créer un menu."""
        response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["nom"] == "Menu Best Of"
    
    def test_preparateur_cannot_create_menu(self, client, preparateur_token, auth_headers, sample_menu_data):
        """❌ Un préparateur ne peut pas créer de menu."""
        response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_superviseur_cannot_create_menu(self, client, superviseur_token, auth_headers, sample_menu_data):
        """❌ Un superviseur ne peut pas créer de menu."""
        response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_accueil_cannot_create_menu(self, client, accueil_token, auth_headers, sample_menu_data):
        """❌ Un agent d'accueil ne peut pas créer de menu."""
        response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_unauthenticated_cannot_create_menu(self, client, sample_menu_data):
        """❌ Sans authentification, impossible de créer un menu."""
        response = client.post("/menus/", json=sample_menu_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # ==========================================
    # Tests de la route GET /menus/ (Liste)
    # ==========================================
    
    def test_anyone_can_list_menus(self, client):
        """✅ La liste des menus est accessible sans authentification."""
        response = client.get("/menus/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
    
    def test_authenticated_user_can_list_menus(self, client, preparateur_token, auth_headers):
        """✅ Un utilisateur authentifié peut lister les menus."""
        response = client.get(
            "/menus/",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    # ==========================================
    # Tests de la route GET /menus/available
    # ==========================================
    
    def test_anyone_can_list_available_menus(self, client):
        """✅ La liste des menus disponibles est publique."""
        response = client.get("/menus/available")
        assert response.status_code == status.HTTP_200_OK
    
    # ==========================================
    # Tests de la route GET /menus/{menu_id}
    # ==========================================
    
    def test_anyone_can_view_menu(self, client, admin_token, auth_headers, sample_menu_data):
        """✅ Consulter un menu est public."""
        # Créer un menu
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]
        
        # Consulter sans authentification
        response = client.get(f"/menus/{menu_id}")
        assert response.status_code == status.HTTP_200_OK
    
    # ==========================================
    # Tests de la route PUT /menus/{menu_id}
    # ==========================================
    
    def test_admin_can_update_menu(self, client, admin_token, auth_headers, sample_menu_data):
        """✅ Un administrateur peut modifier un menu."""
        # Créer un menu
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]
        
        # Modifier le menu
        update_data = {"nom": "Menu Best Of Updated"}
        response = client.put(
            f"/menus/{menu_id}",
            json=update_data,
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["nom"] == "Menu Best Of Updated"
    
    def test_preparateur_cannot_update_menu(self, client, admin_token, preparateur_token, auth_headers, sample_menu_data):
        """❌ Un préparateur ne peut pas modifier un menu."""
        # Créer un menu
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]
        
        # Tenter de modifier
        update_data = {"nom": "Hacked"}
        response = client.put(
            f"/menus/{menu_id}",
            json=update_data,
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_superviseur_cannot_update_menu(self, client, admin_token, superviseur_token, auth_headers, sample_menu_data):
        """❌ Un superviseur ne peut pas modifier un menu."""
        # Créer un menu
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]
        
        # Tenter de modifier
        update_data = {"nom": "Hacked"}
        response = client.put(
            f"/menus/{menu_id}",
            json=update_data,
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route PATCH /menus/{id}/toggle-availability
    # ==========================================
    
    def test_admin_can_toggle_availability(self, client, admin_token, auth_headers, sample_menu_data):
        """✅ Un administrateur peut basculer la disponibilité."""
        # Créer un menu
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]
        
        # Basculer la disponibilité
        response = client.patch(
            f"/menus/{menu_id}/toggle-availability",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_superviseur_can_toggle_availability(self, client, admin_token, superviseur_token, auth_headers, sample_menu_data):
        """✅ Un superviseur peut basculer la disponibilité."""
        # Créer un menu
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]
        
        # Basculer la disponibilité
        response = client.patch(
            f"/menus/{menu_id}/toggle-availability",
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_preparateur_cannot_toggle_availability(self, client, admin_token, preparateur_token, auth_headers, sample_menu_data):
        """❌ Un préparateur ne peut pas basculer la disponibilité."""
        # Créer un menu
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]
        
        # Tenter de basculer
        response = client.patch(
            f"/menus/{menu_id}/toggle-availability",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_accueil_cannot_toggle_availability(self, client, admin_token, accueil_token, auth_headers, sample_menu_data):
        """❌ Un agent d'accueil ne peut pas basculer la disponibilité."""
        # Créer un menu
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]
        
        # Tenter de basculer
        response = client.patch(
            f"/menus/{menu_id}/toggle-availability",
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route POST /menus/{id}/products
    # ==========================================
    
    def test_admin_can_add_products_to_menu(self, client, admin_token, auth_headers, sample_menu_data, sample_product_data):
        """✅ Un administrateur peut ajouter des produits à un menu."""
        # Créer un menu
        menu_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = menu_response.json()["id"]
        
        # Créer un produit
        product_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = product_response.json()["id"]
        
        # Ajouter le produit au menu
        response = client.post(
            f"/menus/{menu_id}/products",
            json=[product_id],
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_superviseur_cannot_add_products_to_menu(self, client, admin_token, superviseur_token, auth_headers, sample_menu_data, sample_product_data):
        """❌ Un superviseur ne peut pas ajouter des produits à un menu."""
        # Créer un menu et un produit
        menu_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = menu_response.json()["id"]
        
        product_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = product_response.json()["id"]
        
        # Tenter d'ajouter
        response = client.post(
            f"/menus/{menu_id}/products",
            json=[product_id],
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route DELETE /menus/{id}/products
    # ==========================================
    
    def test_admin_can_remove_products_from_menu(self, client, admin_token, auth_headers, sample_menu_data, sample_product_data):
        """✅ Un administrateur peut retirer des produits d'un menu."""
        # Créer un menu et un produit
        menu_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = menu_response.json()["id"]
        
        product_response = client.post(
            "/products/",
            json=sample_product_data,
            headers=auth_headers(admin_token)
        )
        product_id = product_response.json()["id"]
        
        # Ajouter puis retirer le produit
        client.post(
            f"/menus/{menu_id}/products",
            json=[product_id],
            headers=auth_headers(admin_token)
        )
        
        response = client.delete(
            f"/menus/{menu_id}/products",
            json=[product_id],
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_preparateur_cannot_remove_products_from_menu(self, client, admin_token, preparateur_token, auth_headers, sample_menu_data):
        """❌ Un préparateur ne peut pas retirer des produits d'un menu."""
        # Créer un menu
        menu_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = menu_response.json()["id"]
        
        # Tenter de retirer
        response = client.delete(
            f"/menus/{menu_id}/products",
            json=[1],
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route DELETE /menus/{menu_id}
    # ==========================================
    
    def test_admin_can_delete_menu(self, client, admin_token, auth_headers, sample_menu_data):
        """✅ Un administrateur peut supprimer un menu."""
        # Créer un menu
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]
        
        # Supprimer le menu
        response = client.delete(
            f"/menus/{menu_id}",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_superviseur_cannot_delete_menu(self, client, admin_token, superviseur_token, auth_headers, sample_menu_data):
        """❌ Un superviseur ne peut pas supprimer un menu."""
        # Créer un menu
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]
        
        # Tenter de supprimer
        response = client.delete(
            f"/menus/{menu_id}",
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_preparateur_cannot_delete_menu(self, client, admin_token, preparateur_token, auth_headers, sample_menu_data):
        """❌ Un préparateur ne peut pas supprimer un menu."""
        # Créer un menu
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]
        
        # Tenter de supprimer
        response = client.delete(
            f"/menus/{menu_id}",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_accueil_cannot_delete_menu(self, client, admin_token, accueil_token, auth_headers, sample_menu_data):
        """❌ Un agent d'accueil ne peut pas supprimer un menu."""
        # Créer un menu
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]
        
        # Tenter de supprimer
        response = client.delete(
            f"/menus/{menu_id}",
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

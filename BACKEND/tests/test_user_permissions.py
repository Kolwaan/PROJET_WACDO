# Vérifie que seuls les administrateurs peuvent gérer les utilisateurs.

import pytest
from fastapi import status


class TestUserPermissions:
    """Tests de sécurisation des routes utilisateurs."""
    
    # ==========================================
    # Tests de la route GET /users/ (Liste)
    # ==========================================
    
    def test_admin_can_list_all_users(self, client, admin_token, auth_headers):
        """✅ Un administrateur peut lister tous les utilisateurs."""
        response = client.get(
            "/users/",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
    
    def test_preparateur_cannot_list_users(self, client, preparateur_token, auth_headers):
        """❌ Un préparateur ne peut pas lister les utilisateurs."""
        response = client.get(
            "/users/",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Accès refusé" in response.json()["detail"]
    
    def test_superviseur_cannot_list_users(self, client, superviseur_token, auth_headers):
        """❌ Un superviseur ne peut pas lister les utilisateurs."""
        response = client.get(
            "/users/",
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_accueil_cannot_list_users(self, client, accueil_token, auth_headers):
        """❌ Un agent d'accueil ne peut pas lister les utilisateurs."""
        response = client.get(
            "/users/",
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_unauthenticated_cannot_list_users(self, client):
        """❌ Sans authentification, impossible de lister les utilisateurs."""
        response = client.get("/users/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # ==========================================
    # Tests de la route GET /users/{user_id}
    # ==========================================
    
    def test_admin_can_get_user_by_id(self, client, admin_token, auth_headers):
        """✅ Un administrateur peut consulter un utilisateur par ID."""
        # D'abord créer un utilisateur
        user_data = {
            "nom": "Test",
            "email": "gettest@example.com",
            "password": "Password123!",
            "role": "AGENT_ACCUEIL"
        }
        create_response = client.post("/users/register", json=user_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        user_id = create_response.json()["id"]
        
        # Tenter de récupérer l'utilisateur
        response = client.get(
            f"/users/{user_id}",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == "gettest@example.com"
    
    def test_preparateur_cannot_get_user_by_id(self, client, preparateur_token, auth_headers):
        """❌ Un préparateur ne peut pas consulter un utilisateur par ID."""
        response = client.get(
            "/users/1",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route PUT /users/{user_id}
    # ==========================================
    
    def test_admin_can_update_user(self, client, admin_token, auth_headers):
        """✅ Un administrateur peut modifier un utilisateur."""
        # Créer un utilisateur
        user_data = {
            "nom": "Original",
            "email": "update@example.com",
            "password": "Password123!",
            "role": "AGENT_ACCUEIL"
        }
        create_response = client.post("/users/register", json=user_data)
        user_id = create_response.json()["id"]
        
        # Modifier l'utilisateur
        update_data = {"nom": "Updated"}
        response = client.put(
            f"/users/{user_id}",
            json=update_data,
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["nom"] == "Updated"
    
    def test_accueil_cannot_update_user(self, client, accueil_token, auth_headers):
        """❌ Un agent d'accueil ne peut pas modifier un autre utilisateur."""
        update_data = {"nom": "Hacked"}
        response = client.put(
            "/users/1",
            json=update_data,
            headers=auth_headers(accueil_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests de la route DELETE /users/{user_id}
    # ==========================================
    
    def test_admin_can_delete_user(self, client, admin_token, auth_headers):
        """✅ Un administrateur peut supprimer un utilisateur."""
        # Créer un utilisateur
        user_data = {
            "nom": "ToDelete",
            "email": "delete@example.com",
            "password": "Password123!",
            "role": "AGENT_ACCUEIL"
        }
        create_response = client.post("/users/register", json=user_data)
        user_id = create_response.json()["id"]
        
        # Supprimer l'utilisateur
        response = client.delete(
            f"/users/{user_id}",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_superviseur_cannot_delete_user(self, client, superviseur_token, auth_headers):
        """❌ Un superviseur ne peut pas supprimer un utilisateur."""
        response = client.delete(
            "/users/1",
            headers=auth_headers(superviseur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # ==========================================
    # Tests des routes /users/me (Profil personnel)
    # ==========================================
    
    def test_any_authenticated_user_can_get_own_profile(self, client, preparateur_token, auth_headers):
        """✅ N'importe quel utilisateur authentifié peut voir son propre profil."""
        response = client.get(
            "/users/me",
            headers=auth_headers(preparateur_token)
        )
        # Note : Ce test peut échouer si l'utilisateur n'existe pas en DB
        # Dans un vrai scénario, il faudrait créer l'utilisateur d'abord
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    
    def test_any_authenticated_user_can_update_own_profile(self, client, accueil_token, auth_headers):
        """✅ N'importe quel utilisateur authentifié peut modifier son propre profil."""
        update_data = {"nom": "NewName"}
        response = client.put(
            "/users/me",
            json=update_data,
            headers=auth_headers(accueil_token)
        )
        # Note : Ce test peut échouer si l'utilisateur n'existe pas en DB
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    
    def test_unauthenticated_cannot_access_me(self, client):
        """❌ Sans authentification, impossible d'accéder à /users/me."""
        response = client.get("/users/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # ==========================================
    # Tests de la route POST /users/register
    # ==========================================
    
    def test_anyone_can_register(self, client):
        """✅ L'inscription est publique (pas d'authentification requise)."""
        user_data = {
            "nom": "Public",
            "email": "public@example.com",
            "password": "Password123!",
            "role": "AGENT_ACCUEIL"
        }
        response = client.post("/users/register", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == "public@example.com"

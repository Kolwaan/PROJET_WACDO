# Tests de sécurisation des routes utilisateurs avec emails uniques

import pytest
from fastapi import status
from uuid import uuid4


class TestUserPermissions:

    # ==========================================
    # Créer un utilisateur POST /users/register (uniquement admin)
    # ==========================================

    # L'admin peut créer un utilisateur
    def test_admin_can_register_user(self, client, admin_token, auth_headers):
        email = f"nouvel_{uuid4().hex}@example.com"
        user_data = {
            "nom": "NouvelUtilisateur",
            "email": email,
            "password": "Password123!",
            "role": "AGENT_ACCUEIL"
        }
        response = client.post(
            "/users/register",
            json=user_data,
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == email

    # Les non-admin ne peuvent pas créer un utilisateur
    def test_non_admin_cannot_register_user(self, client, preparateur_token, auth_headers):
        email = f"hack_{uuid4().hex}@example.com"
        user_data = {
            "nom": "TentativeHacker",
            "email": email,
            "password": "Password123!",
            "role": "AGENT_ACCUEIL"
        }
        response = client.post(
            "/users/register",
            json=user_data,
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Liste des utilisateurs GET /users/
    # ==========================================

    def test_admin_can_list_all_users(self, client, admin_token, auth_headers):
        response = client.get("/users/", headers=auth_headers(admin_token))
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_non_admin_cannot_list_users(self, client, preparateur_token, auth_headers):
        response = client.get("/users/", headers=auth_headers(preparateur_token))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_list_users(self, client):
        response = client.get("/users/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # ==========================================
    # Consulter un utilisateur GET /users/{user_id}
    # ==========================================

    def test_admin_can_get_user_by_id(self, client, admin_token, auth_headers):
        # Créer un utilisateur avec email unique
        email = f"gettest_{uuid4().hex}@example.com"
        user_data = {
            "nom": "Test",
            "email": email,
            "password": "Password123!",
            "role": "AGENT_ACCUEIL"
        }
        create_response = client.post("/users/register", json=user_data, headers=auth_headers(admin_token))
        assert create_response.status_code == status.HTTP_201_CREATED
        user_id = create_response.json()["id"]

        # Récupérer l'utilisateur par ID
        response = client.get(f"/users/{user_id}", headers=auth_headers(admin_token))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == email

    def test_non_admin_cannot_get_user_by_id(self, client, preparateur_token, auth_headers):
        response = client.get("/users/1", headers=auth_headers(preparateur_token))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Modifier un utilisateur PUT /users/{user_id}
    # ==========================================

    def test_admin_can_update_user(self, client, admin_token, auth_headers):
        email = f"update_{uuid4().hex}@example.com"
        user_data = {
            "nom": "Original",
            "email": email,
            "password": "Password123!",
            "role": "AGENT_ACCUEIL"
        }
        create_response = client.post("/users/register", json=user_data, headers=auth_headers(admin_token))
        assert create_response.status_code == status.HTTP_201_CREATED
        user_id = create_response.json()["id"]

        # Modifier l'utilisateur
        response = client.put(f"/users/{user_id}", json={"nom": "Updated"}, headers=auth_headers(admin_token))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["nom"] == "Updated"

    def test_non_admin_cannot_update_other_user(self, client, accueil_token, auth_headers):
        response = client.put("/users/1", json={"nom": "Hacked"}, headers=auth_headers(accueil_token))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Supprimer un utilisateur DELETE /users/{user_id}
    # ==========================================

    def test_admin_can_delete_user(self, client, admin_token, auth_headers):
        email = f"delete_{uuid4().hex}@example.com"
        user_data = {
            "nom": "ToDelete",
            "email": email,
            "password": "Password123!",
            "role": "AGENT_ACCUEIL"
        }
        create_response = client.post("/users/register", json=user_data, headers=auth_headers(admin_token))
        assert create_response.status_code == status.HTTP_201_CREATED
        user_id = create_response.json()["id"]

        response = client.delete(f"/users/{user_id}", headers=auth_headers(admin_token))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_non_admin_cannot_delete_user(self, client, superviseur_token, auth_headers):
        response = client.delete("/users/1", headers=auth_headers(superviseur_token))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Profil personnel /users/me
    # ==========================================

    def test_authenticated_user_can_get_own_profile(self, client, preparateur_token, auth_headers):
        response = client.get("/users/me", headers=auth_headers(preparateur_token))
        assert response.status_code == status.HTTP_200_OK

    def test_authenticated_user_can_update_own_profile(self, client, accueil_token, auth_headers):
        response = client.put("/users/me", json={"nom": "NewName"}, headers=auth_headers(accueil_token))
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_cannot_access_me(self, client):
        response = client.get("/users/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

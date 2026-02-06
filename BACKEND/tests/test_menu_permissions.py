# Tests essentiels de gestion des menus

import pytest
from fastapi import status


class TestMenuPermissions:

    # ==========================================
    # Tests de la route POST /menus/ (Création)
    # ==========================================

    # Un administrateur peut créer un menu.
    def test_admin_can_create_menu(self, client, admin_token, auth_headers, sample_menu_data):
        response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["nom"] == "Menu Best Of"

    # Un utilisateur non admin ne peut pas créer de menu.
    def test_non_admin_cannot_create_menu(self, client, preparateur_token, auth_headers, sample_menu_data):
        response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # Un utilisateur non authentifié ne peut pas créer de menu.
    def test_unauthenticated_cannot_create_menu(self, client, sample_menu_data):
        response = client.post("/menus/", json=sample_menu_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED



    # ==========================================
    # Tests de la route GET /menus/ (Liste)
    # ==========================================

    # La liste des menus est publique.
    def test_anyone_can_list_menus(self, client):
        response = client.get("/menus/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    # Un utilisateur authentifié peut aussi lister les menus.
    def test_authenticated_user_can_list_menus(self, client, preparateur_token, auth_headers):
        response = client.get(
            "/menus/",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_200_OK

    # ==========================================
    # Tests de la route GET /menus/{menu_id}
    # ==========================================

    # Consulter un menu est public.
    def test_anyone_can_view_menu(self, client, admin_token, auth_headers, sample_menu_data):
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
    # Tests de la route PUT /menus/{menu_id} (Modification)
    # ==========================================

    # Un administrateur peut modifier un menu.
    def test_admin_can_update_menu(self, client, admin_token, auth_headers, sample_menu_data):
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]

        update_data = {"nom": "Menu Best Of Updated"}
        response = client.put(
            f"/menus/{menu_id}",
            json=update_data,
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["nom"] == "Menu Best Of Updated"

    # Un utilisateur non admin ne peut pas modifier un menu.
    def test_non_admin_cannot_update_menu(self, client, admin_token, preparateur_token, auth_headers, sample_menu_data):
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]

        update_data = {"nom": "Hacked"}
        response = client.put(
            f"/menus/{menu_id}",
            json=update_data,
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # ==========================================
    # Tests de la route DELETE /menus/{menu_id}
    # ==========================================

    # Un administrateur peut supprimer un menu.
    def test_admin_can_delete_menu(self, client, admin_token, auth_headers, sample_menu_data):
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]

        response = client.delete(
            f"/menus/{menu_id}",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    # Un utilisateur non admin ne peut pas supprimer un menu.
    def test_non_admin_cannot_delete_menu(self, client, admin_token, preparateur_token, auth_headers, sample_menu_data):
        create_response = client.post(
            "/menus/",
            json=sample_menu_data,
            headers=auth_headers(admin_token)
        )
        menu_id = create_response.json()["id"]

        response = client.delete(
            f"/menus/{menu_id}",
            headers=auth_headers(preparateur_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

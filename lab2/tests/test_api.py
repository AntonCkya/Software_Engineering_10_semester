import pytest  # noqa
import time


class TestAuthEndpoints:
    def test_register_user(self, client, test_user_data):
        response = client.post("/api/v1/auth/register", json=test_user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["login"] == test_user_data["login"]
        assert data["first_name"] == test_user_data["first_name"]
        assert data["last_name"] == test_user_data["last_name"]
        assert data["email"] == test_user_data["email"]
        assert "id" in data
        assert "password" not in data

    def test_register_duplicate_login(self, client, test_user_data, registered_user):
        response = client.post("/api/v1/auth/register", json=test_user_data)

        assert response.status_code == 400

    def test_login_success(self, client, test_user_data, registered_user):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "login": test_user_data["login"],
                "password": test_user_data["password"],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user_data, registered_user):
        response = client.post(
            "/api/v1/auth/login",
            json={"login": test_user_data["login"], "password": "wrong_password"},
        )

        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={"login": "nonexistent", "password": "password123"},
        )

        assert response.status_code == 401

    def test_refresh_token_success(self, client, auth_tokens):
        refresh_token = auth_tokens["refresh_token"]
        time.sleep(2) # хак, чтобы у токенов точно отличалось expire

        response = client.post(
            "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["access_token"] != auth_tokens["access_token"]
        assert data["refresh_token"] != auth_tokens["refresh_token"]

    def test_refresh_token_invalid(self, client):
        response = client.post(
            "/api/v1/auth/refresh", json={"refresh_token": "invalid_token"}
        )

        assert response.status_code == 401

    def test_refresh_token_access_token_instead(self, client, auth_tokens):
        response = client.post(
            "/api/v1/auth/refresh", json={"refresh_token": auth_tokens["access_token"]}
        )

        assert response.status_code == 401


class TestUserEndpoints:
    def test_get_user_by_login(self, client, registered_user):
        response = client.get(f"/api/v1/users/login/{registered_user['login']}")

        assert response.status_code == 200
        data = response.json()
        assert data["login"] == registered_user["login"]

    def test_get_user_by_login_not_found(self, client):
        response = client.get("/api/v1/users/login/nonexistent")

        assert response.status_code == 404

    def test_search_users_by_first_name(self, client, registered_user):
        client.post(
            "/api/v1/auth/register",
            json={
                "login": "test_user2",
                "first_name": "Testing",
                "last_name": "User2",
                "email": "test2@example.com",
                "password": "password123",
            },
        )

        response = client.post(
            "/api/v1/users/search", json={"first_name_mask": "Test*"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert len(data["users"]) >= 1

    def test_search_users_by_last_name(self, client, registered_user):
        response = client.post("/api/v1/users/search", json={"last_name_mask": "*User"})

        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    def test_search_users_no_mask(self, client):
        response = client.post("/api/v1/users/search", json={})

        assert response.status_code == 400

    def test_get_current_user(self, client, auth_token):
        response = client.get(
            "/api/v1/users/me", headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["login"] == "test_user"

    def test_get_current_user_unauthorized(self, client):
        response = client.get("/api/v1/users/me")

        assert response.status_code == 401


class TestParcelEndpoints:
    def test_create_parcel(self, client, auth_token, registered_user):
        parcel_data = {
            "owner_id": registered_user["id"],
            "description": "Test parcel",
            "weight_kg": 2.5,
            "dimensions": "30x20x10 cm",
        }

        response = client.post(
            "/api/v1/parcels",
            json=parcel_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["owner_id"] == registered_user["id"]
        assert data["description"] == parcel_data["description"]
        assert "tracking_number" in data

    def test_create_parcel_invalid_owner(self, client, auth_token):
        parcel_data = {
            "owner_id": "nonexistent-id",
            "description": "Test parcel",
            "weight_kg": 2.5,
            "dimensions": "30x20x10 cm",
        }

        response = client.post(
            "/api/v1/parcels",
            json=parcel_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 400

    def test_create_parcel_unauthorized(self, client, registered_user):
        parcel_data = {
            "owner_id": registered_user["id"],
            "description": "Test parcel",
            "weight_kg": 2.5,
            "dimensions": "30x20x10 cm",
        }

        response = client.post("/api/v1/parcels", json=parcel_data)

        assert response.status_code == 401

    def test_get_parcel_by_id(self, client, auth_token, registered_user):
        create_response = client.post(
            "/api/v1/parcels",
            json={
                "owner_id": registered_user["id"],
                "description": "Test parcel",
                "weight_kg": 2.5,
                "dimensions": "30x20x10 cm",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        parcel_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/parcels/{parcel_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 200
        assert response.json()["id"] == parcel_id

    def test_get_user_parcels(self, client, auth_token, registered_user):
        client.post(
            "/api/v1/parcels",
            json={
                "owner_id": registered_user["id"],
                "description": "Test parcel",
                "weight_kg": 2.5,
                "dimensions": "30x20x10 cm",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        response = client.get(
            f"/api/v1/parcels/user/{registered_user['id']}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert len(data["parcels"]) >= 1


class TestDeliveryEndpoints:
    def test_create_delivery(self, client, auth_token, registered_user):
        recipient_response = client.post(
            "/api/v1/auth/register",
            json={
                "login": "recipient_user",
                "first_name": "Recipient",
                "last_name": "User",
                "email": "recipient@example.com",
                "password": "password123",
            },
        )
        recipient_id = recipient_response.json()["id"]

        parcel_response = client.post(
            "/api/v1/parcels",
            json={
                "owner_id": registered_user["id"],
                "description": "Test parcel",
                "weight_kg": 2.5,
                "dimensions": "30x20x10 cm",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        parcel_id = parcel_response.json()["id"]

        delivery_data = {
            "sender_id": registered_user["id"],
            "recipient_id": recipient_id,
            "parcel_id": parcel_id,
            "sender_address": "123 Main St, Moscow",
            "recipient_address": "456 Oak Ave, St. Petersburg",
        }

        response = client.post(
            "/api/v1/deliveries",
            json=delivery_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["sender_id"] == registered_user["id"]
        assert data["recipient_id"] == recipient_id
        assert data["parcel_id"] == parcel_id
        assert data["status"] == "pending"

    def test_create_delivery_invalid_sender(self, client, auth_token, registered_user):
        recipient_response = client.post(
            "/api/v1/auth/register",
            json={
                "login": "recipient_user2",
                "first_name": "Recipient",
                "last_name": "User",
                "email": "recipient2@example.com",
                "password": "password123",
            },
        )
        recipient_id = recipient_response.json()["id"]

        parcel_response = client.post(
            "/api/v1/parcels",
            json={
                "owner_id": registered_user["id"],
                "description": "Test parcel",
                "weight_kg": 2.5,
                "dimensions": "30x20x10 cm",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        parcel_id = parcel_response.json()["id"]

        response = client.post(
            "/api/v1/deliveries",
            json={
                "sender_id": "nonexistent-sender",
                "recipient_id": recipient_id,
                "parcel_id": parcel_id,
                "sender_address": "123 Main St",
                "recipient_address": "456 Oak Ave",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 403

    def test_get_delivery_by_id(self, client, auth_token, registered_user):
        recipient_response = client.post(
            "/api/v1/auth/register",
            json={
                "login": "recipient_user3",
                "first_name": "Recipient",
                "last_name": "User",
                "email": "recipient3@example.com",
                "password": "password123",
            },
        )
        recipient_id = recipient_response.json()["id"]

        parcel_response = client.post(
            "/api/v1/parcels",
            json={
                "owner_id": registered_user["id"],
                "description": "Test parcel",
                "weight_kg": 2.5,
                "dimensions": "30x20x10 cm",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        parcel_id = parcel_response.json()["id"]

        create_response = client.post(
            "/api/v1/deliveries",
            json={
                "sender_id": registered_user["id"],
                "recipient_id": recipient_id,
                "parcel_id": parcel_id,
                "sender_address": "123 Main St",
                "recipient_address": "456 Oak Ave",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        delivery_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/deliveries/{delivery_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 200
        assert response.json()["id"] == delivery_id

    def test_get_deliveries_by_sender(self, client, auth_token, registered_user):
        recipient_response = client.post(
            "/api/v1/auth/register",
            json={
                "login": "recipient_user4",
                "first_name": "Recipient",
                "last_name": "User",
                "email": "recipient4@example.com",
                "password": "password123",
            },
        )
        recipient_id = recipient_response.json()["id"]

        parcel_response = client.post(
            "/api/v1/parcels",
            json={
                "owner_id": registered_user["id"],
                "description": "Test parcel",
                "weight_kg": 2.5,
                "dimensions": "30x20x10 cm",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        parcel_id = parcel_response.json()["id"]

        client.post(
            "/api/v1/deliveries",
            json={
                "sender_id": registered_user["id"],
                "recipient_id": recipient_id,
                "parcel_id": parcel_id,
                "sender_address": "123 Main St",
                "recipient_address": "456 Oak Ave",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        response = client.get(
            f"/api/v1/deliveries/sender/{registered_user['id']}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    def test_get_deliveries_by_recipient(self, client, auth_token, registered_user):
        recipient_response = client.post(
            "/api/v1/auth/register",
            json={
                "login": "recipient_user5",
                "first_name": "Recipient",
                "last_name": "User",
                "email": "recipient5@example.com",
                "password": "password123",
            },
        )
        recipient_id = recipient_response.json()["id"]
        parcel_response = client.post(
            "/api/v1/parcels",
            json={
                "owner_id": registered_user["id"],
                "description": "Test parcel",
                "weight_kg": 2.5,
                "dimensions": "30x20x10 cm",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        parcel_id = parcel_response.json()["id"]

        client.post(
            "/api/v1/deliveries",
            json={
                "sender_id": registered_user["id"],
                "recipient_id": recipient_id,
                "parcel_id": parcel_id,
                "sender_address": "123 Main St",
                "recipient_address": "456 Oak Ave",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        response = client.get(
            f"/api/v1/deliveries/recipient/{recipient_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

from app.storage import user_repository, parcel_repository, delivery_repository
from main import app

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings

get_settings.cache_clear()


@pytest.fixture(scope="function")
def client():
    user_repository._users = {}
    user_repository._login_index = {}
    parcel_repository._parcels = {}
    parcel_repository._tracking_index = {}
    delivery_repository._deliveries = {}

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_user_data():
    return {
        "login": "test_user",
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "password123",
    }


@pytest.fixture
def second_test_user_data():
    return {
        "login": "test_user2",
        "first_name": "Testing",
        "last_name": "User2",
        "email": "test2@example.com",
        "password": "password456",
    }


@pytest.fixture
def registered_user(client, test_user_data):
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def auth_tokens(client, test_user_data, registered_user):
    login_response = client.post(
        "/api/v1/auth/login",
        json={"login": test_user_data["login"], "password": test_user_data["password"]},
    )
    assert login_response.status_code == 200
    return login_response.json()


@pytest.fixture
def auth_token(client, test_user_data, registered_user):
    login_response = client.post(
        "/api/v1/auth/login",
        json={"login": test_user_data["login"], "password": test_user_data["password"]},
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


@pytest.fixture
def test_settings():
    from app.config import get_settings

    return get_settings()

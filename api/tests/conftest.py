import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client_admin(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username="admin tester",
        email="atest@example.com",
        password="pass123",
        role="admin"
    )
    api_client.force_authenticate(user=user)
    return api_client, user

@pytest.fixture
def auth_client_user(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username="user tester",
        email="utest@example.com",
        password="pass123",
        role="user"
    )
    api_client.force_authenticate(user=user)
    return api_client, user

@pytest.fixture
def auth_client_manager(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username="manager tester",
        email="mtest@example.com",
        password="pass123",
        role="manager"
    )
    api_client.force_authenticate(user=user)
    return api_client, user

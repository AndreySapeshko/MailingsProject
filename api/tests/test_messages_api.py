import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from mailings.tests.factories import MessageFactory, UserFactory

URL = reverse("api:message-list")

# ------------------------------------------------------
# USER TESTS
# ------------------------------------------------------

@pytest.mark.django_db
def test_user_can_create_message(auth_client_user):
    client, user = auth_client_user

    payload = {
        "subject": "Hello",
        "body": "Text"
    }

    response = client.post(URL, payload, format="json")

    assert response.status_code == 201
    assert user.messages.filter(subject="Hello").exists()


@pytest.mark.django_db
def test_user_sees_only_his_messages(auth_client_user):
    client, user = auth_client_user

    # свои
    MessageFactory.create_batch(2, user=user)

    # чужие
    MessageFactory.create_batch(3)

    res = client.get(URL)

    assert res.status_code == 200
    assert res.data["count"] == 2


@pytest.mark.django_db
def test_user_can_update_own_message(auth_client_user):
    client, user = auth_client_user
    msg = MessageFactory(user=user)

    res = client.patch(f"{URL}{msg.id}/", {"subject": "Updated"}, format="json")

    assert res.status_code == 200
    msg.refresh_from_db()
    assert msg.subject == "Updated"


@pytest.mark.django_db
def test_user_cannot_update_foreign_message(auth_client_user):
    client, user = auth_client_user
    msg = MessageFactory()  # чужой

    res = client.patch(f"{URL}{msg.id}/", {"subject": "Hack"}, format="json")

    assert res.status_code == 404


# ------------------------------------------------------
# MANAGER TESTS
# ------------------------------------------------------

@pytest.mark.django_db
def test_manager_can_view_all(auth_client_manager):
    client, mgr = auth_client_manager

    MessageFactory.create_batch(5)

    res = client.get(URL)

    assert res.status_code == 200
    assert res.data["count"] == 5


@pytest.mark.django_db
def test_manager_cannot_create(auth_client_manager):
    client, mgr = auth_client_manager

    payload = {"subject": "X", "body": "Y"}

    res = client.post(URL, payload, format="json")

    assert res.status_code == 403


@pytest.mark.django_db
def test_manager_cannot_update(auth_client_manager):
    client, mgr = auth_client_manager
    msg = MessageFactory()

    res = client.patch(f"{URL}{msg.id}/", {"subject": "Edit"}, format="json")

    assert res.status_code == 403


# ------------------------------------------------------
# ADMIN TESTS
# ------------------------------------------------------

@pytest.mark.django_db
def test_admin_can_edit_any(auth_client_admin):
    client, admin = auth_client_admin
    msg = MessageFactory()

    res = client.patch(f"{URL}{msg.id}/", {"subject": "Admin Edit"}, format="json")

    assert res.status_code == 200
    msg.refresh_from_db()
    assert msg.subject == "Admin Edit"


@pytest.mark.django_db
def test_admin_can_delete_any(auth_client_admin):
    client, admin = auth_client_admin
    msg = MessageFactory()

    res = client.delete(f"{URL}{msg.id}/")

    assert res.status_code == 204
    assert not MessageFactory._meta.model.objects.filter(id=msg.id).exists()

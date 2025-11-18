import pytest
from mailings.models import Message
from mailings.tests.factories import MessageFactory
from django.urls import reverse

URL = reverse("api:message-list")  # если у тебя другой namespace — скажи

# -------------------------------
# USER — создаёт, редактирует, удаляет только свои
# -------------------------------

@pytest.mark.django_db
def test_user_can_create_message(auth_client_user):
    client, user = auth_client_user
    payload = {"subject": "test title", "body": "test body"}

    r = client.post(URL, payload)
    assert r.status_code == 201
    assert Message.objects.filter(user=user).count() == 1


@pytest.mark.django_db
def test_user_can_only_see_own_message(auth_client_user):
    client, user = auth_client_user

    MessageFactory.create_batch(2, user=user)
    MessageFactory.create_batch(3)  # чужие

    r = client.get(URL)
    assert r.status_code == 200
    assert r.json()["count"] == 2


@pytest.mark.django_db
def test_user_cannot_edit_foreign(auth_client_user):
    client, user = auth_client_user
    msg = MessageFactory()  # чужой

    r = client.patch(f"{URL}{msg.id}/", {"subject": "Hack"})
    assert r.status_code == 404  # скрываем объект


@pytest.mark.django_db
def test_user_cannot_delete_foreign(auth_client_user):
    client, user = auth_client_user
    msg = MessageFactory()

    r = client.delete(f"{URL}{msg.id}/")
    assert r.status_code == 404

# -------------------------------
# MANAGER — видит всё, менять ничего не может
# -------------------------------

@pytest.mark.django_db
def test_manager_can_view_all(auth_client_manager):
    client, manager = auth_client_manager

    MessageFactory.create_batch(5)

    r = client.get(URL)
    assert r.status_code == 200
    assert r.json()["count"] == 5


@pytest.mark.django_db
def test_manager_cannot_edit(auth_client_manager):
    client, manager = auth_client_manager
    msg = MessageFactory()

    r = client.patch(f"{URL}{msg.id}/", {"subject": "Hack"})
    assert r.status_code in [403, 405]  # зависит от правил


@pytest.mark.django_db
def test_manager_cannot_delete(auth_client_manager):
    client, manager = auth_client_manager
    msg = MessageFactory()

    r = client.delete(f"{URL}{msg.id}/")
    assert r.status_code == 403

# -------------------------------
# ADMIN — полный доступ
# -------------------------------

@pytest.mark.django_db
def test_admin_can_edit_any(auth_client_admin):
    client, admin = auth_client_admin
    msg = MessageFactory()

    r = client.patch(f"{URL}{msg.id}/", {"subject": "Admin Edit"}, format="json")
    assert r.status_code == 200
    msg.refresh_from_db()
    assert msg.subject == "Admin Edit"


@pytest.mark.django_db
def test_admin_can_delete_any(auth_client_admin):
    client, admin = auth_client_admin
    msg = MessageFactory()

    r = client.delete(f"{URL}{msg.id}/")
    assert r.status_code == 204

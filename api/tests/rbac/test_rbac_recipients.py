import pytest
from recipients.models import Recipient
from recipients.tests.factories import RecipientFactory
from django.urls import reverse

URL = reverse("api:recipient-list")  # если у тебя другой namespace — скажи

# -------------------------------
# USER — создаёт, редактирует, удаляет только свои
# -------------------------------

@pytest.mark.django_db
def test_user_can_create_recipient(auth_client_user):
    client, user = auth_client_user
    payload = {"email": "u@test.com", "name": "User", "comment": "test"}

    r = client.post(URL, payload)
    assert r.status_code == 201
    assert Recipient.objects.filter(user=user).count() == 1


@pytest.mark.django_db
def test_user_can_only_see_own_recipients(auth_client_user):
    client, user = auth_client_user

    RecipientFactory.create_batch(2, user=user)
    RecipientFactory.create_batch(3)  # чужие

    r = client.get(URL)
    assert r.status_code == 200
    assert r.json()["count"] == 2


@pytest.mark.django_db
def test_user_cannot_edit_foreign(auth_client_user):
    client, user = auth_client_user
    recipient = RecipientFactory()  # чужой

    r = client.patch(f"{URL}{recipient.id}/", {"name": "Hack"})
    assert r.status_code == 404  # скрываем объект


@pytest.mark.django_db
def test_user_cannot_delete_foreign(auth_client_user):
    client, user = auth_client_user
    recipient = RecipientFactory()

    r = client.delete(f"{URL}{recipient.id}/")
    assert r.status_code == 404

# -------------------------------
# MANAGER — видит всё, менять ничего не может
# -------------------------------

@pytest.mark.django_db
def test_manager_can_view_all(auth_client_manager):
    client, manager = auth_client_manager

    RecipientFactory.create_batch(5)

    r = client.get(URL)
    assert r.status_code == 200
    assert r.json()["count"] == 5


@pytest.mark.django_db
def test_manager_cannot_edit(auth_client_manager):
    client, manager = auth_client_manager
    rcp = RecipientFactory()

    r = client.patch(f"{URL}{rcp.id}/", {"name": "Hack"})
    assert r.status_code in [403, 405]  # зависит от правил


@pytest.mark.django_db
def test_manager_cannot_delete(auth_client_manager):
    client, manager = auth_client_manager
    rcp = RecipientFactory()

    r = client.delete(f"{URL}{rcp.id}/")
    assert r.status_code == 403

# -------------------------------
# ADMIN — полный доступ
# -------------------------------

@pytest.mark.django_db
def test_admin_can_edit_any(auth_client_admin):
    client, admin = auth_client_admin
    rcp = RecipientFactory()

    r = client.patch(f"{URL}{rcp.id}/", {"name": "Admin Edit"}, format="json")
    assert r.status_code == 200
    rcp.refresh_from_db()
    assert rcp.name == "Admin Edit"


@pytest.mark.django_db
def test_admin_can_delete_any(auth_client_admin):
    client, admin = auth_client_admin
    rcp = RecipientFactory()

    r = client.delete(f"{URL}{rcp.id}/")
    assert r.status_code == 204

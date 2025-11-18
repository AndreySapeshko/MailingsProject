import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from recipients.tests.factories import RecipientFactory
from mailings.tests.factories import (
    UserFactory,
    MailingFactory,
    MessageFactory,
)
from mailings.models import Mailing
from django.utils import timezone


MAILINGS_URL = "/api/mailings/"


# ============================================================
# LIST
# ============================================================

@pytest.mark.django_db
def test_list_only_user_mailings(auth_client_user):
    client, user = auth_client_user

    # свои
    MailingFactory.create_batch(2, user=user)

    # чужие
    MailingFactory.create_batch(3)

    response = client.get(MAILINGS_URL)

    assert response.status_code == 200
    assert response.json().get("count") == 2


@pytest.mark.django_db
def test_manager_sees_all(auth_client_manager):
    client, user = auth_client_manager

    MailingFactory.create_batch(5)

    response = client.get(MAILINGS_URL)

    assert response.status_code == 200
    assert response.json().get("count") == 5


@pytest.mark.django_db
def test_admin_sees_all(auth_client_admin):
    client, user = auth_client_admin

    MailingFactory.create_batch(4)
    response = client.get(MAILINGS_URL)

    assert response.status_code == 200
    assert response.json().get("count") == 4

# ============================================================
# CREATE
# ============================================================

@pytest.mark.django_db
def test_user_can_create_mailing(auth_client_user):
    client, user = auth_client_user

    msg = MessageFactory(user=user)
    rcp = RecipientFactory(user=user)

    payload = {
        "name": "Test Mailing",
        "date_first_dispatch": timezone.now().isoformat(),
        "dispatch_end_date": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
        "status": "created",
        "message": msg.id,
        "recipients": [rcp.id]
    }

    response = client.post(MAILINGS_URL, payload, format="json")

    assert response.status_code == 201
    assert Mailing.objects.filter(name="Test Mailing", user=user).exists()


@pytest.mark.django_db
def test_manager_cannot_create(auth_client_manager):
    client, _ = auth_client_manager

    payload = {"name": "X"}
    response = client.post(MAILINGS_URL, payload, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_create(auth_client_admin):
    client, admin = auth_client_admin

    msg = MessageFactory(user=admin)
    rcp = RecipientFactory(user=admin)

    payload = {
        "name": "Admin Mailing",
        "date_first_dispatch": timezone.now().isoformat(),
        "dispatch_end_date": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
        "status": "created",
        "message": msg.id,
        "recipients": [rcp.id]
    }

    response = client.post(MAILINGS_URL, payload, format="json")

    assert response.status_code == 201
    assert Mailing.objects.filter(name="Admin Mailing").exists()

# ============================================================
# UPDATE
# ============================================================

@pytest.mark.django_db
def test_user_can_update_own(auth_client_user):
    client, user = auth_client_user
    mailing = MailingFactory(user=user)

    response = client.patch(f"{MAILINGS_URL}{mailing.id}/", {"name": "Updated"}, format="json")

    assert response.status_code == 200
    mailing.refresh_from_db()
    assert mailing.name == "Updated"


@pytest.mark.django_db
def test_user_cannot_update_foreign(auth_client_user):
    client, user = auth_client_user
    mailing = MailingFactory()  # чужой

    response = client.patch(f"{MAILINGS_URL}{mailing.id}/", {"name": "Hack"}, format="json")

    assert response.status_code == 404


@pytest.mark.django_db
def test_manager_cannot_update(auth_client_manager):
    client, _ = auth_client_manager
    mailing = MailingFactory()

    response = client.patch(f"{MAILINGS_URL}{mailing.id}/", {"name": "Hack"}, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_update(auth_client_admin):
    client, _ = auth_client_admin
    mailing = MailingFactory()

    response = client.patch(f"{MAILINGS_URL}{mailing.id}/", {"name": "AdminEdit"}, format="json")

    assert response.status_code == 200

# ============================================================
# DELETE
# ============================================================

@pytest.mark.django_db
def test_user_can_delete_own(auth_client_user):
    client, user = auth_client_user
    mailing = MailingFactory(user=user)

    response = client.delete(f"{MAILINGS_URL}{mailing.id}/")

    assert response.status_code == 204
    assert not Mailing.objects.filter(id=mailing.id).exists()


@pytest.mark.django_db
def test_user_cannot_delete_foreign(auth_client_user):
    client, _ = auth_client_user
    mailing = MailingFactory()

    response = client.delete(f"{MAILINGS_URL}{mailing.id}/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_manager_cannot_delete(auth_client_manager):
    client, _ = auth_client_manager
    mailing = MailingFactory()

    response = client.delete(f"{MAILINGS_URL}{mailing.id}/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_delete_any(auth_client_admin):
    client, _ = auth_client_admin
    mailing = MailingFactory()

    response = client.delete(f"{MAILINGS_URL}{mailing.id}/")

    assert response.status_code == 204
    assert not Mailing.objects.filter(id=mailing.id).exists()
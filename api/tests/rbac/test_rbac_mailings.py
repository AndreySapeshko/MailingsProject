import pytest
from mailings.models import Mailing
from mailings.tests.factories import MailingFactory, MessageFactory
from recipients.tests.factories import RecipientFactory
from django.urls import reverse
from django.utils import timezone

URL = reverse("api:mailing-list")  # если у тебя другой namespace — скажи

# -------------------------------
# USER — создаёт, редактирует, удаляет только свои
# -------------------------------

@pytest.mark.django_db
def test_user_can_create_mailing(auth_client_user):
    client, user = auth_client_user
    msg = MessageFactory()
    rcp = RecipientFactory()
    payload = {
        "name": "Test Mailing",
        "date_first_dispatch": timezone.now().isoformat(),
        "dispatch_end_date": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
        "status": "created",
        "message": msg.id,
        "recipients": [rcp.id]
    }

    r = client.post(URL, payload)
    assert r.status_code == 201
    assert Mailing.objects.filter(user=user).count() == 1


@pytest.mark.django_db
def test_user_can_only_see_own_mailing(auth_client_user):
    client, user = auth_client_user

    MailingFactory.create_batch(2, user=user)
    MailingFactory.create_batch(3)  # чужие

    r = client.get(URL)
    assert r.status_code == 200
    assert r.json()["count"] == 2


@pytest.mark.django_db
def test_user_cannot_edit_foreign(auth_client_user):
    client, user = auth_client_user
    mailing = MailingFactory()  # чужой

    r = client.patch(f"{URL}{mailing.id}/", {"name": "Hack"})
    assert r.status_code == 404  # скрываем объект


@pytest.mark.django_db
def test_user_cannot_delete_foreign(auth_client_user):
    client, user = auth_client_user
    mailing = MailingFactory()

    r = client.delete(f"{URL}{mailing.id}/")
    assert r.status_code == 404

# -------------------------------
# MANAGER — видит всё, менять ничего не может
# -------------------------------

@pytest.mark.django_db
def test_manager_can_view_all(auth_client_manager):
    client, manager = auth_client_manager

    MailingFactory.create_batch(5)

    r = client.get(URL)
    assert r.status_code == 200
    assert r.json()["count"] == 5


@pytest.mark.django_db
def test_manager_cannot_edit(auth_client_manager):
    client, manager = auth_client_manager
    mailing = MailingFactory()

    r = client.patch(f"{URL}{mailing.id}/", {"name": "Hack"})
    assert r.status_code in [403, 405]  # зависит от правил


@pytest.mark.django_db
def test_manager_cannot_delete(auth_client_manager):
    client, manager = auth_client_manager
    mailing = MailingFactory()

    r = client.delete(f"{URL}{mailing.id}/")
    assert r.status_code == 403

# -------------------------------
# ADMIN — полный доступ
# -------------------------------

@pytest.mark.django_db
def test_admin_can_edit_any(auth_client_admin):
    client, admin = auth_client_admin
    mailing = MailingFactory()

    r = client.patch(f"{URL}{mailing.id}/", {"name": "Admin Edit"}, format="json")
    assert r.status_code == 200
    mailing.refresh_from_db()
    assert mailing.name == "Admin Edit"


@pytest.mark.django_db
def test_admin_can_delete_any(auth_client_admin):
    client, admin = auth_client_admin
    mailing = MailingFactory()

    r = client.delete(f"{URL}{mailing.id}/")
    assert r.status_code == 204

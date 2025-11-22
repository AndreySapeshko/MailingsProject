import logging
import pytest
from recipients.models import Recipient
from recipients.tests.factories import RecipientFactory

logger = logging.getLogger('django')

RECIPIENTS_URL = "/api/recipients/"


@pytest.mark.django_db
def test_create_recipient(auth_client_admin):
    client, user = auth_client_admin

    payload = {
        "email": "test@example.com",
        "name": "Test User",
        "comment": "Some comment"
    }

    response = client.post(RECIPIENTS_URL, data=payload, format="json")

    assert response.status_code == 201
    assert Recipient.objects.filter(email="test@example.com").exists()


@pytest.mark.django_db
def test_list_only_user_recipients(auth_client_user):
    client, user = auth_client_user
    # свои
    RecipientFactory.create_batch(2, user=user)

    # чужие
    RecipientFactory.create_batch(3)

    response = client.get(RECIPIENTS_URL)

    assert response.status_code == 200
    logger.info(f'response.json(): {response.json()}')
    assert response.json().get('count') == 2


@pytest.mark.django_db
def test_cannot_create_duplicate_email(auth_client_admin):
    client, user = auth_client_admin

    RecipientFactory(user=user, email="dup@example.com")

    payload = {
        "email": "dup@example.com",
        "name": "Duplicate"
    }

    response = client.post(RECIPIENTS_URL, payload, format="json")

    assert response.status_code in (400, 409)  # зависит от реализации

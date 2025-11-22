import pytest
from unittest.mock import patch

from mailings.tests.factories import MailingFactory
from recipients.tests.factories import RecipientFactory

@pytest.mark.django_db
def test_send_now_is_idempotent(mocker):
    send_mock = mocker.patch("mailings.models.send_mail", return_value=1)

    mailing = MailingFactory()
    r = RecipientFactory(user=mailing.user)
    mailing.recipients.set([r])

    # Первая отправка
    mailing.send_now()
    assert send_mock.call_count == 1

    # Вторая отправка — НЕ должно быть повторного send_mail
    mailing.send_now()
    assert send_mock.call_count == 1


@pytest.mark.django_db
def test_resend_failed_sends_only_failed(mocker):
    send_mock = mocker.patch("mailings.models.send_mail", return_value=1)

    mailing = MailingFactory()

    r1 = RecipientFactory(user=mailing.user)
    r2 = RecipientFactory(user=mailing.user)
    mailing.recipients.set([r1, r2])

    # Симулируем логи: один success, один failed
    from mailings.models import MailingLog
    MailingLog.objects.create(mailing=mailing, recipient=r1, status="success")
    MailingLog.objects.create(mailing=mailing, recipient=r2, status="failed")

    mailing.resend_failed()

    assert send_mock.call_count == 1  # только r2

import pytest
from unittest.mock import patch

from mailings.models import Mailing
from recipients.models import Recipient
from mailings.tests.factories import MailingFactory, MessageFactory, UserFactory
from recipients.tests.factories import RecipientFactory


@pytest.mark.django_db
def test_send_now_sends_email_to_all_recipients(mocker):
    """send_now должен отправлять письмо всем активным получателям."""

    # Создаём пользователей, сообщения и рассылку
    mailing = MailingFactory()

    # Создаём получателей для этого пользователя
    r1 = RecipientFactory(user=mailing.user)
    r2 = RecipientFactory(user=mailing.user)
    r3 = RecipientFactory(user=mailing.user, is_active=False)  # не должен получить письмо
    mailing.recipients.set([r1, r2, r3])

    # Мокаем send_mail
    send_mock = mocker.patch("mailings.models.send_mail", return_value=1)

    # Вызываем основную функцию
    mailing.send_now()

    # Проверяем, что send_mail вызван 2 раза — только для активных
    assert send_mock.call_count == 2

    emails = {call.kwargs["recipient_list"][0] for call in send_mock.call_args_list}
    assert emails == {r1.email, r2.email}


@pytest.mark.django_db
def test_send_now_calls_send_mail_with_correct_args(mocker):
    mailing = MailingFactory()
    recipient = RecipientFactory(user=mailing.user)
    mailing.recipients.set([recipient])

    send_mock = mocker.patch("mailings.models.send_mail", return_value=1)

    mailing.send_now()

    send_mock.assert_called_once()

    call = send_mock.call_args.kwargs

    assert call["subject"] == mailing.message.subject
    assert call["message"] == mailing.message.body
    assert call["recipient_list"] == [recipient.email]


import pytest
from unittest import mock
from mailings.tasks import ping_celery, process_mailings
from mailings.models import Mailing
from django.utils import timezone
from django.conf import settings
from .factories import MailingFactory


@pytest.mark.django_db(transaction=True)
def test_ping_celery_runs_successfully():
    """Проверяет, что простая задача Celery выполняется и возвращает результат."""
    settings.CELERY_TASK_ALWAYS_EAGER = True

    result = ping_celery.delay()
    assert result.get() == "pong"
    assert result.successful()


@pytest.mark.django_db
def test_process_mailings_triggers_only_active(mocker):
    active = MailingFactory()
    inactive = MailingFactory(
        status="finished",
        date_first_dispatch=timezone.now() - timezone.timedelta(days=10),
        dispatch_end_date=timezone.now() - timezone.timedelta(days=5),
    )

    mock = mocker.patch.object(active.__class__, "send_now")

    process_mailings()

    mock.assert_called_once()


@pytest.mark.django_db
def test_process_mailings_skips_inactive(mocker):
    """process_mailings должен пропускать рассылки, у которых статус не 'started'."""

    mailing = MailingFactory(status="created")

    mock = mocker.patch.object(mailing.__class__, "send_now")

    process_mailings()

    mock.assert_not_called()

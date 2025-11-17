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


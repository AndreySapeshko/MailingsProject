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

@pytest.mark.django_db(transaction=True)
def test_process_mailings_handles_exceptions(mocker):
    """Проверяет, что при ошибке внутри send_now задача не падает."""

    # Создаём рассылку, которая должна быть обработана
    mailing = MailingFactory(status="started")

    # Мокаем send_now так, чтобы он кидал исключение
    mocker.patch(
        "mailings.models.Mailing.send_now",
        side_effect=Exception("boom")
    )

    # Запускаем задачу Celery
    result = process_mailings.delay()

    # Задача должна выполниться и НЕ упасть
    result.get(timeout=10)
    assert result.successful()


@pytest.mark.django_db(transaction=True)
def test_process_mailings_handles_exceptions(mocker):
    """Проверяет, что при ошибке внутри send_now задача не падает."""

    # Создаём рассылку, которая должна быть обработана
    mailing = MailingFactory(status="started")

    # Мокаем send_now так, чтобы он кидал исключение
    mocker.patch(
        "mailings.models.Mailing.send_now",
        side_effect=Exception("boom")
    )

    # Запускаем задачу Celery
    result = process_mailings.delay()

    # Задача должна выполниться и НЕ упасть
    result.get(timeout=10)
    assert result.successful()


@pytest.mark.django_db
def test_run_mailing_tasks_calls_process_mailings_delay(mocker):
    delay_mock = mocker.patch("mailings.tasks.process_mailings.delay")

    from scheduler.tasks import run_mailing_tasks
    run_mailing_tasks()

    delay_mock.assert_called_once_with()

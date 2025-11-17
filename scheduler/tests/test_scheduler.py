import pytest

from datetime import datetime, timedelta
from django.utils import timezone
from mailings.tests.factories import MailingFactory


@pytest.mark.django_db
def test_scheduler_triggers_process_mailings(mocker):
    """Проверяем, что планировщик запускает celery-задачу."""

    delay_mock = mocker.patch("mailings.tasks.process_mailings.delay")

    from scheduler.tasks import run_mailing_tasks  # пример

    run_mailing_tasks()  # должен запускать задачу

    delay_mock.assert_called_once()

import pytest

from freezegun import freeze_time
from django.utils import timezone
from datetime import datetime, timezone as tz

from mailings.tasks import process_mailings
from mailings.tests.factories import MailingFactory


@pytest.mark.django_db
def test_process_mailings_runs_inside_time_window(mocker):
    """
    Рассылка с статусом 'started' и окном [start, end]
    должна обрабатываться только если now внутри окна.
    """

    # 1. Создаем рассылку с фиксированным окном
    start = timezone.datetime(2025, 1, 1, 10, 0, tzinfo=tz.utc)
    end = timezone.datetime(2025, 1, 1, 11, 0, tzinfo=tz.utc)

    mailing = MailingFactory(
        status="started",
        date_first_dispatch=start,
        dispatch_end_date=end,
    )

    send_now_mock = mocker.patch("mailings.models.Mailing.send_now")

    # 2. Время внутри окна → задача должна обработать рассылку
    with freeze_time("2025-01-01 10:30:00"):
        process_mailings()

    send_now_mock.assert_called_once_with()

    # 3. Сбрасываем мок и выходим за окно → не должно быть вызовов
    send_now_mock.reset_mock()

    with freeze_time("2025-01-01 11:30:00"):
        process_mailings()

    send_now_mock.assert_not_called()

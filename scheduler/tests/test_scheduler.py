import pytest

from unittest.mock import patch, MagicMock


@pytest.mark.django_db
def test_scheduler_triggers_process_mailings(mocker):
    """Проверяем, что планировщик запускает celery-задачу."""

    delay_mock = mocker.patch("mailings.tasks.process_mailings.delay")

    from scheduler.tasks import run_mailing_tasks  # пример

    run_mailing_tasks()  # должен запускать задачу

    delay_mock.assert_called_once()


def test_scheduler_starts_and_adds_job(mocker):
    """Проверяем, что старт планировщика добавляет нужную задачу."""
    # Мокаем BackgroundScheduler и DjangoJobStore
    scheduler_mock = MagicMock()
    bg_scheduler = mocker.patch("scheduler.scheduler.BackgroundScheduler", return_value=scheduler_mock)
    jobstore_mock = mocker.patch("scheduler.scheduler.DjangoJobStore")

    # Мокаем старт Celery-задачи
    run_task_mock = mocker.patch("scheduler.scheduler.run_mailing_tasks")

    # Эмулируем переменную окружения RUN_MAIN='true'
    mocker.patch.dict("os.environ", {"RUN_MAIN": "true"})

    from scheduler.scheduler import start
    start()

    # Проверяем, что планировщик создан
    bg_scheduler.assert_called_once()

    # Проверяем, что jobstore добавлен
    scheduler_mock.add_jobstore.assert_called_once_with(jobstore_mock(), "default")

    # Проверяем что задача добавлена
    scheduler_mock.add_job.assert_called_once()

    args, kwargs = scheduler_mock.add_job.call_args

    # Проверяем, что вызываем run_mailing_tasks
    assert args[0] == run_task_mock

    # Проверяем, что триггер interval 1 минута
    assert kwargs["trigger"] == "interval"
    assert kwargs["minutes"] == 1
    assert kwargs["id"] == "mailing_scheduler"
    assert kwargs["replace_existing"] is True

    # Проверяем, что стартанул
    scheduler_mock.start.assert_called_once()

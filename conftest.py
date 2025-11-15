import pytest
from celery import Celery
from django.conf import settings


@pytest.fixture(scope="session", autouse=True)
def celery_test_app():
    """
    Полноценный Celery тестовый инстанс.
    Обходит реальный Redis/broker и выполняет задачи синхронно.
    """

    app = Celery("test_celery")
    app.conf.update(
        broker_url="memory://",
        result_backend="cache+memory://",
        task_always_eager=True,
        task_eager_propagates=True,
        task_default_queue="celery",
    )

    # Загружаем задачи из Django-приложений
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

    return app

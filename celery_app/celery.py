import os
import django
from celery import Celery
import logging.config

print(f"🚀 Celery started with {os.environ.get('DJANGO_SETTINGS_MODULE')=}")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailings_project.settings.prod')

# Настройки брокера и результатов (общие для всех)
app = Celery(
    'mailings_core',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
    include=[
        'mailings.tasks',
        'recipients.tasks',
        'scheduler.tasks',
        'accounts.tasks'
    ]
)


print(f"📦 Broker: {app.conf.broker_url}")
print(f"📦 Backend: {app.conf.result_backend}")

app.config_from_object('django.conf:settings', namespace='CELERY')

django.setup()
from django.conf import settings
logging.config.dictConfig(settings.LOGGING)

# Общие параметры
app.conf.update(
    task_default_queue='celery',
    task_default_exchange='celery',
    task_default_routing_key='celery',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Moscow',
    enable_utc=True,
)

app.autodiscover_tasks(
    # lambda: [n.name for n in __import__('django.apps').apps.apps.get_app_configs()]
    [
    'mailings',
    'recipients',
    'scheduler',
    'accounts',
    ]
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# @app.task(name='ping_simple')
# def ping_simple():
#     print('Task ping_simple. Отработала!')
#     return 'ok'


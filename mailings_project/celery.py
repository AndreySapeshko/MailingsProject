import os
from celery import Celery

# Указываем Django настройки
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailings_project.settings.prod')

app = Celery('mailings_project')

# Загружаем конфиг из Django settings с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем таски во всех приложениях
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

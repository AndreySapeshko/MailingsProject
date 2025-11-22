from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
from django.conf import settings


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        try:
            from scheduler import scheduler
            if getattr(settings, "DEBUG", False):
                from .scheduler import start
                print("⚙️ Планировщик запущен (DEBUG)")
                start()
            scheduler.start()
        except (OperationalError, ProgrammingError):
            # База еще не готова — просто пропускаем
            print("⏳ Планировщик не запущен: база данных ещё не готова.")

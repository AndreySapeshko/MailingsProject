from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError

class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        try:
            from scheduler import scheduler
            scheduler.start()
        except (OperationalError, ProgrammingError):
            # База еще не готова — просто пропускаем
            print("⏳ Планировщик не запущен: база данных ещё не готова.")

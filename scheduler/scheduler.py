import os

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from scheduler.tasks import run_mailing_tasks

def start():
    if os.environ.get('RUN_MAIN') != 'true':
        print("⚙️ Планировщик не запущен (вспомогательный процесс runserver).")
        return
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        run_mailing_tasks,
        trigger='interval',
        minutes=1,  # проверять каждую минуту
        id='mailing_scheduler',
        replace_existing=True,
    )

    scheduler.start()
    print("✅ Планировщик запущен (каждую минуту проверяет рассылки).")

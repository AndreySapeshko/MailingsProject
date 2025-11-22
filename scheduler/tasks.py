from mailings.tasks import process_mailings

def run_mailing_tasks():
    """Планировщик запускает задачу Celery."""

    process_mailings.delay()

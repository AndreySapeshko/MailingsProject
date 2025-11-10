from celery import shared_task
from django.utils import timezone
from celery_app.celery import app
from pathlib import Path

import logging


logger = logging.getLogger("celery")

@app.task(name="mailings.tasks.process_mailings")
def process_mailings():
    """Основная Celery-задача — проверяет активные рассылки и запускает их отправку"""
    from mailings.models import Mailing
    now = timezone.now()
    logger.info(f"📬 Проверяю активные рассылки ({now:%Y-%m-%d %H:%M})")

    # Получаем рассылки, которые должны быть активны
    active_mailings = Mailing.objects.filter(
        date_first_dispatch__lte=now,
        dispatch_end_date__gte=now,
        status='started'
    )

    if not active_mailings.exists():
        logger.info("ℹ️ Нет активных рассылок для отправки.")
        return

    for mailing in active_mailings:
        try:
            logger.info(f"🚀 Запуск рассылки {mailing.id} ({mailing.name})")
            mailing.send_now()
            logger.info(f"✅ Рассылка {mailing.id} успешно обработана.")
        except Exception as e:
            logger.exception(f"❌ Ошибка при обработке рассылки {mailing.id}: {e}")

# @shared_task
# def ping_celery():
#     print("🔥 ping_celery() started (print)")
#     logger.info("🔥 ping_celery() started (logger)")
#     msg = "🔥 ping_celery() executed!\n"
#     Path("/tmp/celery_test.txt").write_text(msg)
#     print(msg)
#     return "pong"

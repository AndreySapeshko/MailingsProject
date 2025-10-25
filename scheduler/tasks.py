from datetime import datetime
from django.utils import timezone
from mailings.models import Mailing

def run_mailing_tasks():
    """Проверяет все активные рассылки и отправляет письма по расписанию"""
    now = timezone.now()
    mailings = Mailing.objects.filter(status='launched', dispatch_end_date__gte=now)

    for mailing in mailings:
        # Проверяем, пора ли отправлять
        if mailing.date_first_dispatch <= now:
            print(f"⏰ Отправка рассылки: {mailing.name}")
            mailing.send_now()

            # Пересчитываем следующее время в зависимости от периодичности
            if mailing.periodicity == 'daily':
                mailing.date_first_dispatch += timezone.timedelta(days=1)
            elif mailing.periodicity == 'weekly':
                mailing.date_first_dispatch += timezone.timedelta(weeks=1)
            else:
                # если одноразовая рассылка — завершаем
                mailing.status = 'completed'

            mailing.save(update_fields=['date_first_dispatch', 'status'])

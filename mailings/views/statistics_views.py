from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from mailings.models import MailingLog, Mailing
from users.mixins import AccessByRoleMixin

class MailingStatisticsView(LoginRequiredMixin, AccessByRoleMixin, TemplateView):
    template_name = 'mailings/mailing_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Общие показатели
        if user.is_manager() or user.is_superuser:
            logs = MailingLog.objects.all()
        else:
            logs = MailingLog.objects.filter(mailing__user=user)
        total = logs.count()
        success = logs.filter(status='success').count()
        failed = logs.filter(status='failed').count()

        success_percent = round((success / total * 100), 1) if total else 0
        failed_percent = 100 - success_percent if total else 0

        # Группировка по рассылкам
        per_mailing = (
            logs.values('mailing__name')
            .annotate(
                total=Count('id'),
                success=Count('id', filter=Q(status='success')),
                failed=Count('id', filter=Q(status='failed')),
            )
            .order_by('-total')
        )

        context.update({
            'total': total,
            'success': success,
            'failed': failed,
            'success_percent': success_percent,
            'failed_percent': failed_percent,
            'per_mailing': list(per_mailing),
        })
        return context

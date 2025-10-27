from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from mailings.models import MailingLog
from users.mixins import AccessByRoleMixin

class MailingLogListView(LoginRequiredMixin, AccessByRoleMixin, ListView):
    model = MailingLog
    template_name = 'mailings/mailing_logs.html'
    context_object_name = 'logs'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('mailing', 'recipient')
        mailing_id = self.request.GET.get('mailing')
        if mailing_id:
            qs = qs.filter(mailing_id=mailing_id)
        return qs.order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailings'] = self.request.user.mailings.all()
        context['selected_mailing'] = self.request.GET.get('mailing')
        return context

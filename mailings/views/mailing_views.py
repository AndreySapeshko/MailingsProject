from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from mailings.models import Mailing
from mailings.forms import MailingForm
from users.mixins import AccessByRoleMixin
from core.mixins.cache_mixins import CachedViewMixin


class MailingActionView(LoginRequiredMixin, View):
    """Обработчик кнопок: запуск, остановка, отправка сейчас"""

    def post(self, request, pk, action):
        mailing = get_object_or_404(Mailing, pk=pk, user=request.user)

        if action == 'start':
            mailing.launch()
            messages.success(request, f"Рассылка '{mailing.name}' запущена.")
        elif action == 'stop':
            mailing.stop()
            messages.warning(request, f"Рассылка '{mailing.name}' остановлена.")
        elif action == 'send':
            count = mailing.send_now()
            messages.success(request, f"Отправлено писем: {count}")

        return redirect(reverse('mailings:mailing_list'))


class MailingListView(CachedViewMixin, LoginRequiredMixin, AccessByRoleMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'
    cache_timeout = 600

    def get_queryset(self):
        user = self.request.user
        qs = Mailing.objects.all()
        if not (user.is_superuser or user.role in ['manager', 'admin']):
            qs = qs.filter(user=user)
        return qs


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Рассылка успешно создана.')
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, AccessByRoleMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        messages.success(self.request, 'Рассылка обновлена.')
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, AccessByRoleMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, 'Рассылка удалена.')
        return super().delete(request, *args, **kwargs)

from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from mailings.models import Mailing
from mailings.forms import MailingForm


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


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return Mailing.objects.filter(user=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Рассылка успешно создана.')
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Рассылка обновлена.')
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, 'Рассылка удалена.')
        return super().delete(request, *args, **kwargs)

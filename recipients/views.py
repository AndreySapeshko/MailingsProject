from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Recipient
from .forms import RecipientForm


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'recipients/recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipients/recipient_form.html'
    success_url = reverse_lazy('recipients:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Получатель успешно добавлен.')
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipients/recipient_form.html'
    success_url = reverse_lazy('recipients:list')

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Данные получателя обновлены.')
        return super().form_valid(form)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'recipients/recipient_confirm_delete.html'
    success_url = reverse_lazy('recipients:list')

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, 'Получатель удалён.')
        return super().delete(request, *args, **kwargs)

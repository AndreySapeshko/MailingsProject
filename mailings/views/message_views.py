from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from mailings.models import Message
from mailings.forms import MessageForm


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailings/messages/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/messages/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Шаблон письма успешно создан.')
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/messages/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Шаблон письма обновлён.')
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailings/messages/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, 'Шаблон письма удалён.')
        return super().delete(request, *args, **kwargs)

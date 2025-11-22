from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from mailings.models import Message
from mailings.forms import MessageForm
from users.mixins import AccessByRoleMixin
from core.mixins.cache_mixins import CachedViewMixin


class MessageListView(CachedViewMixin, LoginRequiredMixin, AccessByRoleMixin, ListView):
    model = Message
    template_name = 'mailings/messages/message_list.html'
    context_object_name = 'msgs'
    cache_timeout = 600

    def get_queryset(self):
        user = self.request.user
        qs = Message.objects.all()
        if not (user.is_superuser or user.role in ['manager', 'admin']):
            qs = qs.filter(user=user)
        return qs


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/messages/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Шаблон письма успешно создан.')
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, AccessByRoleMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/messages/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        messages.success(self.request, 'Шаблон письма обновлён.')
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, AccessByRoleMixin, DeleteView):
    model = Message
    template_name = 'mailings/messages/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, 'Шаблон письма удалён.')
        return super().delete(request, *args, **kwargs)

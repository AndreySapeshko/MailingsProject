from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib import messages
from .forms import UserProfileForm
from django.contrib.auth import get_user_model
from .mixins import AccessByRoleMixin

User = get_user_model()

class ProfileView(LoginRequiredMixin, AccessByRoleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлён ✅")
        return super().form_valid(form)

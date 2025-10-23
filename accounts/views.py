from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import RegisterForm, UserUpdateForm


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'


class RegisterUserView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


class ProfileEditView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user


def logout_view(request):
    logout(request)
    return redirect('accounts:login')

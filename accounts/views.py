from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, ProfileForm


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        messages.success(self.request, f'Добро пожаловать, {form.get_user().username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка входа. Проверьте имя пользователя и пароль.')
        return super().form_invalid(form)


class RegisterUserView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        self.object = form.save()
        raw_password = form.cleaned_data.get('password1')

        user = authenticate(
            self.request,
            username=self.object.username,
            password=raw_password
        )
        print("User authenticated:", user)
        print("Backends:", self.request.session.keys())
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Добро пожаловать, {user.username}! Вы успешно зарегистрировались.')
        else:
            messages.warning(self.request, 'Аккаунт создан, но автоматический вход не выполнен.')

        return redirect(self.success_url)


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


class ProfileEditView(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлён.')
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('accounts:login')

from django import forms
from django.contrib.auth import get_user_model
from mailings.forms import StyledFormMixin

User = get_user_model()

class UserProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not (user.is_manager() or user.is_superuser):
            self.fields['role'].disabled = True

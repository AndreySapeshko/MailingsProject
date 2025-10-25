from django import forms
from .models import Recipient
from mailings.forms import StyledFormMixin

class RecipientForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['name', 'email', 'comment']

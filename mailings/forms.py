from django import forms

from recipients.models import Recipient
from .models import Message, Mailing

class StyledFormMixin:
    """Миксин для добавления Bootstrap-классов ко всем полям"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            css_class = 'form-control'
            if visible.field.widget.__class__.__name__ in ('CheckboxInput',):
                css_class = 'form-check-input'
            visible.field.widget.attrs['class'] = css_class


class MessageForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        labels = {
            'subject': 'Тема письма',
            'body': 'Текст письма',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 6}),
        }


class MailingForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = [
            'name',
            'date_first_dispatch',
            'dispatch_end_date',
            'periodicity',
            'recipients',
            'message',
        ]
        labels = {
            'name': 'Название рассылки',
            'date_first_dispatch': 'Дата первой отправки',
            'dispatch_end_date': 'Дата окончания',
            'periodicity': 'Периодичность',
            'recipients': 'Получатели',
            'message': 'Сообщение',
        }
        widgets = {
            'date_first_dispatch': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'dispatch_end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'recipients': forms.SelectMultiple(attrs={'size': 6}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # извлекаем текущего пользователя
        super().__init__(*args, **kwargs)
        if user:
            self.fields['recipients'].queryset = Recipient.objects.filter(user=user)
            self.fields['message'].queryset = Message.objects.filter(user=user)

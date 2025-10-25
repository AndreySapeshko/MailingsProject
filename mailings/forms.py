from django import forms

class StyledFormMixin:
    """Миксин для добавления Bootstrap-классов ко всем полям"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            css_class = 'form-control'
            if visible.field.widget.__class__.__name__ in ('CheckboxInput',):
                css_class = 'form-check-input'
            visible.field.widget.attrs['class'] = css_class

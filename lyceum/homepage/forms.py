from django import forms
from django.utils.translation import gettext_lazy as _

__all__ = []


class EchoForm(forms.Form):
    text = forms.CharField(
        label=_('Введите текст'),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        error_messages={
            'required': _('Пожалуйста, заполните поле.'),
            'invalid': _('Пожалуйста, проверьте данные.'),
        },
    )

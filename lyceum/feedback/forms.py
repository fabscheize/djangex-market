from django import forms
from django.utils.translation import gettext_lazy as _

from feedback.models import Feedback

__all__ = []


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
            if field.errors:
                field.field.widget.attrs['class'] += ' is-invalid'


class FeedbackForm(BaseModelForm):
    class Meta:
        model = Feedback
        exclude = (
            Feedback.id.field.name,
            Feedback.created_on.field.name,
        )
        labels = {
            Feedback.name.field.name: _('Ваше имя'),
            Feedback.mail.field.name: _('Ваша электронная почта'),
            Feedback.text.field.name: _('Ваш вопрос или пожелание'),
        }
        help_texst = {
            Feedback.mail.field.name: 'name@example.com',
        }
        widgets = {
            Feedback.name.field.name: forms.TextInput,
            Feedback.mail.field.name: forms.EmailInput(
                {'placeholder': 'name@example.com'},
            ),
            Feedback.text.field.name: forms.Textarea(
                {'rows': 5},
            ),
        }
        error_messages = {
            Feedback.name.field.name: {
                'required': _('Пожалуйста, укажите Ваше имя.'),
                'invalid': _('Пожалуйста, проверьте данные.'),
            },
            Feedback.mail.field.name: {
                'required': _('Пожалуйста, укажите Вашу электронную почту.'),
                'invalid': _(
                    'Пожалуйста, введите корректный формат электронной почты.',
                ),
            },
            Feedback.text.field.name: {
                'required': _('Пожалуйста, заполните Ваше обращение.'),
                'invalid': _('Пожалуйста, проверьте данные.'),
            },
        }

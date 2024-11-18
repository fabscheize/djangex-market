from django import forms
from django.utils.translation import gettext_lazy as _

from core.forms import BaseModelForm
from feedback import models

__all__ = []


class FeedbackForm(BaseModelForm):
    class Meta:
        model = models.Feedback

        exclude = (
            models.Feedback.status.field.name,
            models.Feedback.created_on.field.name,
        )
        labels = {
            models.Feedback.text.field.name: _('Ваш вопрос или пожелание'),
        }
        help_texts = {
            models.Feedback.text.field.name: _('Обязательное поле'),
        }
        widgets = {
            models.Feedback.text.field.name: forms.Textarea(
                {
                    'rows': 5,
                    'aria-describedby': 'id_textHelp',
                },
            ),
        }
        error_messages = {
            models.Feedback.text.field.name: {
                'required': _('Пожалуйста, заполните Ваше обращение'),
            },
        }


class FeedbackAuthorForm(BaseModelForm):
    class Meta:
        model = models.FeedbackAuthor

        fields = (
            models.FeedbackAuthor.name.field.name,
            models.FeedbackAuthor.mail.field.name,
        )
        labels = {
            models.FeedbackAuthor.name.field.name: _('Ваше имя'),
            models.FeedbackAuthor.mail.field.name: _('Ваша электронная почта'),
        }
        help_texts = {
            models.FeedbackAuthor.mail.field.name: _('Обязательное поле'),
        }
        widgets = {
            models.FeedbackAuthor.name.field.name: forms.TextInput,
            models.FeedbackAuthor.mail.field.name: forms.EmailInput(
                {
                    'placeholder': 'name@example.com',
                    'aria-describedby': 'id_mailHelp',
                },
            ),
        }
        error_messages = {
            models.FeedbackAuthor.mail.field.name: {
                'required': _('Пожалуйста, укажите Вашу электронную почту'),
                'invalid': _(
                    'Пожалуйста, введите корректный формат электронной почты',
                ),
            },
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            'widget',
            MultipleFileInput(attrs={'class': 'form-control'}),
        )
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]

        return [single_file_clean(data, initial)]


class FeedbackFileForm(forms.Form):
    files = MultipleFileField(
        label=_('При необходимости прикрепите файлы'),
        required=False,
    )

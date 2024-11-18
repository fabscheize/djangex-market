from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _

from core.forms import BaseModelForm
from users import models

__all__ = []


class UserCreationForm(BaseModelForm, auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm):
        model = models.User

        fields = [
            models.User.username.field.name,
            models.User.email.field.name,
        ]
        labels = {
            models.User.username.field.name: _('Никнейм'),
            models.User.email.field.name: _('Почта'),
        }
        help_texts = {
            models.User.email.field.name: _('Обязательное поле.'),
        }


class UserChangeForm(BaseModelForm):
    class Meta(auth_forms.UserChangeForm):
        model = models.User

        fields = [
            models.User.first_name.field.name,
            models.User.last_name.field.name,
            models.User.email.field.name,
        ]
        labels = {
            models.User.first_name.field.name: _('Имя'),
            models.User.last_name.field.name: _('Фамилия'),
            models.User.email.field.name: _('Почта'),
        }


class ProfileForm(BaseModelForm):
    class Meta:
        model = models.Profile

        fields = [
            models.Profile.birthday.field.name,
            models.Profile.image.field.name,
        ]
        labels = {
            models.Profile.birthday.field.name: _('Дата рождения'),
            models.Profile.image.field.name: _('Изменить аватар'),
        }
        widgets = {
            models.Profile.birthday.field.name: forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
            'image': forms.FileInput(
                attrs={'class': 'form-control', 'accept': 'image/*'},
            ),
        }

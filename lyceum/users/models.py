import uuid

from django.contrib.auth.models import User
import django.core.validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseImageModel

__all__ = []


class Profile(BaseImageModel):
    def avatar_directory_path(self, filename):
        return f'avatars/{self.user_id}/{uuid.uuid4()}-{filename}'

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('пользователь'),
    )
    birthday = models.DateField(
        verbose_name=_('дата рождения'),
        auto_now=False,
        auto_now_add=False,
    )
    coffee_count = models.IntegerField(
        verbose_name=_('счетчик кофе'),
        blank=False,
        default=0,
    )
    image = django.db.models.ImageField(
        upload_to=avatar_directory_path,
        verbose_name=_('аватар'),
        default=None,
    )

    class Meta:
        verbose_name = _('профиль пользователя')
        verbose_name_plural = _('профили пользователей')

    def __str__(self):
        return self.user.username

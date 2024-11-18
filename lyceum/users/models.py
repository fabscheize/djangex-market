import sys
import uuid

from django.contrib.auth.models import User
import django.core.validators
from django.db import models
from django.db.models.fields.related import ReverseOneToOneDescriptor
from django.utils.translation import gettext_lazy as _

from core.models import BaseImageModel

__all__ = []

if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
    User._meta.get_field('email')._unique = True


class AutoReverseOneToOneDescriptor(ReverseOneToOneDescriptor):
    def __get__(self, instance, instance_type=None):
        try:
            return super(AutoReverseOneToOneDescriptor, self).__get__(
                instance,
                instance_type,
            )
        except self.related.related_model.DoesNotExist:
            related_model = self.related.related_model
            obj = related_model(**{self.related.field.name: instance})
            obj.save()
            return obj


class AutoOneToOneField(models.OneToOneField):
    def contribute_to_related_class(self, cls, related):
        setattr(
            cls,
            related.get_accessor_name(),
            AutoReverseOneToOneDescriptor(related),
        )


class Profile(BaseImageModel):
    def avatar_directory_path(self, filename):
        return f'avatars/{self.user_id}/{uuid.uuid4()}-{filename}'

    user = AutoOneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('пользователь'),
    )
    birthday = models.DateField(
        verbose_name=_('дата рождения'),
        blank=True,
        null=True,
    )
    coffee_count = models.IntegerField(
        verbose_name=_('счетчик кофе'),
        default=0,
    )
    image = django.db.models.ImageField(
        upload_to=avatar_directory_path,
        verbose_name=_('аватар'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('профиль пользователя')
        verbose_name_plural = _('профили пользователей')

    def __str__(self):
        return self.user.username

import uuid

from django.core.files.storage import default_storage
import django.core.validators
import django.db.models
import django.utils.safestring
from django.utils.translation import gettext_lazy as _
import sorl.thumbnail

__all__ = []


def image_directory_path(instance, filename):
    return f'catalog/{instance.item.id}/{uuid.uuid4()}-{filename}'


class BaseSaleModel(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name=_('название'),
        help_text=_('Максимум 150 символов'),
        max_length=150,
        unique=True,
    )
    is_published = django.db.models.BooleanField(
        verbose_name=_('опубликовано'),
        default=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name if len(self.name) <= 21 else self.name[:18] + '...'


class BaseImageModel(django.db.models.Model):
    image = django.db.models.ImageField(
        upload_to=image_directory_path,
        verbose_name=_('изображение'),
        default=None,
    )

    class Meta:
        abstract = True

    @property
    def is_image(self):
        return self.image and default_storage.exists(self.image.name)

    def _thumb_image(self, size: int):
        if self.is_image:
            return sorl.thumbnail.get_thumbnail(
                self.image,
                f'{size}x{size}',
                crop='center',
                quality=60,
            )

        return None

    @property
    def get_image_50x50(self):
        return self._thumb_image(50)

    def get_image_300x300(self):
        return self._thumb_image(300)

    def get_image_800x800(self):
        return self._thumb_image(800)

    def display_image_300x300(self):
        if self.is_image:
            return django.utils.safestring.mark_safe(
                f'<img src="{self.get_image_300x300().url}" '
                'width="{300}" height="{300}" />',
            )

        return _('Нет изображения')

    display_image_300x300.short_description = _('превью')
    display_image_300x300.allow_tags = True

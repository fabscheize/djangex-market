import uuid

import django.core.files.base
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
        verbose_name=_('title'),
        help_text=_('Max 150 symbols'),
        max_length=150,
        unique=True,
    )

    is_published = django.db.models.BooleanField(
        verbose_name=_('published'),
        default=True,
    )

    def __str__(self):
        return self.name if len(self.name) <= 21 else self.name[:18] + '...'

    class Meta:
        abstract = True


class BaseImageModel(django.db.models.Model):
    image = django.db.models.ImageField(
        upload_to=image_directory_path,
        verbose_name=_('image'),
        default=None,
    )

    def _thumb_image(self, size: int):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            f'{size}x{size}',
            crop='center',
            quality=60,
        )

    @property
    def get_image_50x50(self):
        return self._thumb_image(50)

    def get_image_300x300(self):
        return self._thumb_image(300)

    def get_image_800x800(self):
        return self._thumb_image(800)

    def display_image_300x300(self):
        if self.image:
            return django.utils.safestring.mark_safe(
                f'<img src="{self.get_image_300x300().url}" '
                'width="{500}" height="{500}" />',
            )
        return _('No image')

    display_image_300x300.short_description = _('preview')
    display_image_300x300.allow_tags = True

    class Meta:
        abstract = True

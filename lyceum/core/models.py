import uuid

import django.core.validators
import django.db.models
import django.utils.safestring
import sorl.thumbnail

__all__ = []


def image_directory_path(instance, filename):
    return f'catalog/{instance.item.id}/{uuid.uuid4()}-{filename}'


class BaseSaleModel(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name='название',
        help_text='Максимум 150 символов',
        max_length=150,
        unique=True,
    )

    is_published = django.db.models.BooleanField(
        verbose_name='опубликовано',
        default=True,
    )

    def __str__(self):
        return self.name if len(self.name) <= 15 else self.name[:12] + '...'

    class Meta:
        abstract = True


class BaseImageModel(django.db.models.Model):
    image = django.db.models.ImageField(
        upload_to=image_directory_path,
        verbose_name='изображение',
        default=None,
    )

    def _thumb_image(self, size: int):
        thumb = sorl.thumbnail.get_thumbnail(
            self.image,
            f'{size}x{size}',
            crop='center',
            quality=60,
        )

        return django.utils.safestring.mark_safe(
            f'<img src="{thumb.url}" width="{size}" height="{size}" />',
        )

    def get_image_300x300(self):
        return self._thumb_image(300) if self.image else 'Нет изображения'

    @property
    def get_image_50x50(self):
        return self._thumb_image(50)

    get_image_300x300.short_description = 'превью'
    get_image_300x300.allow_tags = True

    class Meta:
        abstract = True

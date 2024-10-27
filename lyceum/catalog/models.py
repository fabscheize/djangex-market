import re

from django.core import exceptions, validators
from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from transliterate import translit

from catalog.validators import ValidateContainsWords
from core.models import AbstractModel

__all__ = []

PUNCTUATION_REGEX = re.compile(r'[\W_]')


def normalize_name(name):
    name = re.sub(PUNCTUATION_REGEX, '', name).lower()
    name = translit(name, 'ru', reversed=True)
    return name


def thumb_image(image):
    thumb = get_thumbnail(
        image,
        '300x300',
        crop='center',
        quality=75,
    )
    return mark_safe(
        f'<img src="{thumb.url}" width="300" height="300" />',
    )


class Category(AbstractModel):
    slug = models.SlugField(
        verbose_name='слаг',
        max_length=200,
        unique=True,
        help_text=(
            'Только латинские буквы, цифры, знаки подчеркивания или дефиса'
        ),
    )
    weight = models.IntegerField(
        verbose_name='вес',
        default=100,
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(32767),
        ],
    )
    normalized_name = models.CharField(
        verbose_name='нормализованное имя',
        max_length=150,
        unique=True,
        editable=False,
    )

    def clean(self):
        normalized = normalize_name(self.name)
        if (
            not self.pk
            and Category.objects.filter(normalized_name=normalized).exists()
        ):
            raise exceptions.ValidationError(
                {'name': 'Категория с похожим именем уже существует.'},
            )

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Tag(AbstractModel):
    slug = models.SlugField(
        verbose_name='слаг',
        max_length=200,
        unique=True,
        help_text=(
            'Только латинские буквы, цифры, знаки подчеркивания или дефиса'
        ),
    )
    normalized_name = models.CharField(
        verbose_name='нормализованное имя',
        max_length=150,
        unique=True,
        editable=False,
    )

    def clean(self):
        normalized = normalize_name(self.name)
        if (
            not self.pk
            and Tag.objects.filter(normalized_name=normalized).exists()
        ):
            raise exceptions.ValidationError(
                {'name': 'Тег с похожим именем уже существует.'},
            )

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Item(AbstractModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='категория',
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='теги',
    )

    text = models.TextField(
        verbose_name='текст',
        help_text=(
            'В описании обязательно должно быть слово '
            '"превосходно" или "роскошно"'
        ),
        validators=[
            ValidateContainsWords('превосходно', 'роскошно'),
        ],
    )

    def get_main_image(self):
        if hasattr(self, 'main_image_obj') and self.main_image_obj.image:
            return thumb_image(self.main_image_obj.image)
        return 'Нет изображения'

    get_main_image.short_description = 'превью'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class MainImage(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name='main_image_obj',
        verbose_name='товар',
    )

    image = models.ImageField(
        upload_to='items/main_images/',
        verbose_name='главное изображение',
        null=True,
        blank=True,
    )

    def get_image(self):
        return thumb_image(self.image) if self.image else 'Нет изображения'

    get_image.short_description = 'превью'
    get_image.allow_tags = True

    class Meta:
        verbose_name = 'главное изображение'
        verbose_name_plural = 'главные изображения'


class ItemImage(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='товар',
    )

    image = models.ImageField(
        upload_to='items/images/',
        verbose_name='изображение',
        null=True,
        blank=True,
    )

    def get_image(self):
        return thumb_image(self.image) if self.image else 'Нет изображения'

    get_image.short_description = 'превью'
    get_image.allow_tags = True

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

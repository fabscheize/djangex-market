import re

from django.core import exceptions, validators
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from tinymce import models as tinymce_models
from transliterate import translit

from catalog.validators import ValidateContainsWords
from core.models import BaseImageModel, BaseSaleModel

__all__ = []

PUNCTUATION_REGEX = re.compile(r'[\W_]')


def normalize_name(name):
    name = re.sub(PUNCTUATION_REGEX, '', name).lower()
    return translit(name, 'ru', reversed=True)


class ItemManager(models.Manager):
    def _item_main_fields(self):
        tags_prefetch = models.Prefetch(
            Item.tags.field.name,
            queryset=Tag.objects.only(Tag.name.field.name).filter(
                is_published=True,
            ),
        )

        return (
            self.get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
            )
            .select_related(
                Item.category.field.name,
                Item.main_image.related.name,
            )
            .prefetch_related(tags_prefetch)
            .only(
                Item.name.field.name,
                Item.text.field.name,
                f'{Item.category.field.name}__{Category.name.field.name}',
                f'{Item.main_image.related.name}'
                f'__{ItemMainImage.image.field.name}',
            )
        )

    def published(self):
        return self._item_main_fields().order_by(
            f'{Item.category.field.name}__{Category.name.field.name}',
            Item.name.field.name,
        )

    def on_main(self):
        return (
            self._item_main_fields()
            .filter(is_on_main=True)
            .order_by(Item.name.field.name, Item.id.field.name)
        )

    def item_detailed(self):
        gallery_prefetch = models.Prefetch(
            Item.images.rel.related_name,
            queryset=ItemImageGallery.objects.only(
                ItemImageGallery.id.field.name,
                ItemImageGallery.item_id.field.name,
                ItemImageGallery.image.field.name,
            ),
        )
        return self._item_main_fields().prefetch_related(gallery_prefetch)


class Category(BaseSaleModel):
    slug = models.SlugField(
        verbose_name=_('слаг'),
        max_length=200,
        unique=True,
        help_text=(
            _(
                'Только латинские буквы, цифры, '
                'знаки подчеркивания или дефиса. ',
            )
            + _('Максимум 200 символов')
        ),
    )
    weight = models.IntegerField(
        verbose_name=_('вес'),
        default=100,
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(32767),
        ],
        help_text=_('Значение от 1 до 32767'),
    )
    normalized_name = models.CharField(
        verbose_name=_('нормализованное имя'),
        max_length=150,
        unique=False,
        editable=False,
    )

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('категории')

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        normalized = normalize_name(self.name)
        if (
            not self.pk
            and Category.objects.filter(normalized_name=normalized).exists()
        ):
            raise exceptions.ValidationError(
                {'name': _('Категория с похожим именем уже существует.')},
            )


class Tag(BaseSaleModel):
    slug = models.SlugField(
        verbose_name=_('слаг'),
        max_length=200,
        unique=True,
        help_text=(
            _(
                'Только латинские буквы, цифры, '
                'знаки подчеркивания или дефиса. ',
            )
            + _('Максимум 200 символов')
        ),
    )
    normalized_name = models.CharField(
        verbose_name=_('нормализованное имя'),
        max_length=150,
        unique=False,
        editable=False,
    )

    class Meta:
        verbose_name = _('тег')
        verbose_name_plural = _('теги')

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        normalized = normalize_name(self.name)
        if (
            not self.pk
            and Tag.objects.filter(normalized_name=normalized).exists()
        ):
            raise exceptions.ValidationError(
                {'name': _('Тег с похожим именем уже существует.')},
            )


class Item(BaseSaleModel):
    is_on_main = models.BooleanField(
        verbose_name=_('на главной'),
        default=False,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_('категория'),
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('теги'),
    )
    text = tinymce_models.HTMLField(
        verbose_name=_('текст'),
        validators=[
            ValidateContainsWords('превосходно', 'роскошно'),
        ],
        help_text=(
            _(
                'В описании обязательно должно быть слово '
                "'превосходно' или 'роскошно'",
            )
        ),
    )
    created = models.DateTimeField(
        verbose_name=_('время создания'),
        auto_now_add=True,
        null=True,
    )
    updated = models.DateTimeField(
        verbose_name=_('время изменения'),
        auto_now=True,
        null=True,
    )

    objects = ItemManager()

    class Meta:
        verbose_name = _('товар')
        verbose_name_plural = _('товары')
        default_related_name = 'items'

    def display_main_image(self):
        if self.main_image.is_image:
            return mark_safe(
                f'<img src="{self.main_image.get_image_50x50.url}" '
                'width="{50}" height="{50}" />',
            )
        return _('Нет изображения')

    display_main_image.short_description = _('превью')
    display_main_image.allow_tags = True


class ItemMainImage(BaseImageModel):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name='main_image',
        verbose_name=_('товар'),
    )

    class Meta:
        verbose_name = _('главное изображение')
        verbose_name_plural = _('главные изображения')

    def __str__(self):
        return self.item.name


class ItemImageGallery(BaseImageModel):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('товар'),
    )

    class Meta:
        verbose_name = _('изображение')
        verbose_name_plural = _('изображения')

    def __str__(self):
        return f'{self.item.name} - {self.id}'

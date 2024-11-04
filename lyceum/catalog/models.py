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
            'tags',
            queryset=Tag.objects.only('name').filter(is_published=True),
        )

        return (
            self.get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
            )
            .select_related(
                'category',
                'main_image',
            )
            .prefetch_related(tags_prefetch)
            .only(
                'name',
                'text',
                'category__name',
                'main_image__image',
            )
        )

    def published(self):
        return self._item_main_fields().order_by('category__name', 'name')

    def on_main(self):
        return (
            self._item_main_fields()
            .filter(is_on_main=True)
            .order_by('name', 'id')
        )

    def item_detailed(self):
        gallery_prefetch = models.Prefetch(
            'images',
            queryset=ItemImageGallery.objects.only('id', 'item_id', 'image'),
        )
        return self._item_main_fields().prefetch_related(gallery_prefetch)


class Category(BaseSaleModel):
    slug = models.SlugField(
        verbose_name=_('slug'),
        max_length=200,
        unique=True,
        help_text=(_('Only latin letters, numbers, underscores or hyphens')),
    )
    weight = models.IntegerField(
        verbose_name=_('weight'),
        default=100,
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(32767),
        ],
    )

    normalized_name = models.CharField(
        verbose_name=_('normalized name'),
        max_length=150,
        unique=False,
        editable=False,
    )

    def clean(self):
        normalized = normalize_name(self.name)
        if (
            not self.pk
            and Category.objects.filter(normalized_name=normalized).exists()
        ):
            raise exceptions.ValidationError(
                {'name': _('A category with a similar name already exists.')},
            )

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Tag(BaseSaleModel):
    slug = models.SlugField(
        verbose_name=_('slug'),
        max_length=200,
        unique=True,
        help_text=(_('Only latin letters, numbers, underscores or hyphens')),
    )

    normalized_name = models.CharField(
        verbose_name=_('normalized name'),
        max_length=150,
        unique=False,
        editable=False,
    )

    def clean(self):
        normalized = normalize_name(self.name)
        if (
            not self.pk
            and Tag.objects.filter(normalized_name=normalized).exists()
        ):
            raise exceptions.ValidationError(
                {'name': _('A tag with a similar name already exists.')},
            )

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class Item(BaseSaleModel):
    objects = ItemManager()

    is_on_main = models.BooleanField(
        verbose_name=_('on main'),
        default=False,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_query_name='items',
        verbose_name=_('category'),
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('tags'),
    )

    text = tinymce_models.HTMLField(
        verbose_name=_('text'),
        help_text=(
            _('The description should contain "превосходно" or "роскошно"')
        ),
        validators=[
            ValidateContainsWords('превосходно', 'роскошно'),
        ],
    )

    def display_main_image(self):
        if hasattr(self, 'main_image'):
            return mark_safe(
                f'<img src="{self.main_image.get_image_50x50.url}" '
                'width="{50}" height="{50}" />',
            )
        return _('No image')

    display_main_image.short_description = _('preview')
    display_main_image.allow_tags = True

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')


class ItemMainImage(BaseImageModel):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name='main_image',
        verbose_name=_('item'),
    )

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = _('main image')
        verbose_name_plural = _('main images')


class ItemImageGallery(BaseImageModel):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('item'),
    )

    def __str__(self):
        return f'{self.item.name} - {self.id}'

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

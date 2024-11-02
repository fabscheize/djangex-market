import re

from django.core import exceptions, validators
from django.db import models
from tinymce import models as tinymce_models
from transliterate import translit

from catalog.validators import ValidateContainsWords
from core.models import BaseImageModel, BaseSaleModel

__all__ = []

PUNCTUATION_REGEX = re.compile(r'[\W_]')


def normalize_name(name):
    name = re.sub(PUNCTUATION_REGEX, '', name).lower()
    name = translit(name, 'ru', reversed=True)
    return name


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
            'image_gallery',
            queryset=ItemImageGallery.objects.only('id', 'item_id', 'image'),
        )
        return self._item_main_fields().prefetch_related(gallery_prefetch)


class Category(BaseSaleModel):
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


class Tag(BaseSaleModel):
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


class Item(BaseSaleModel):
    objects = ItemManager()

    is_on_main = models.BooleanField(
        verbose_name='на главной',
        default=False,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='категория',
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='теги',
    )

    text = tinymce_models.HTMLField(
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
        if hasattr(self, 'main_image'):
            return self.main_image.get_image_50x50
        return 'Нет изображения'

    get_main_image.short_description = 'превью'
    get_main_image.allow_tags = True

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class ItemMainImage(BaseImageModel):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name='main_image',
        verbose_name='товар',
    )

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = 'главное изображение'
        verbose_name_plural = 'главные изображения'


class ItemImageGallery(BaseImageModel):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='image_gallery',
        verbose_name='товар',
    )

    def __str__(self):
        return f'{self.item.name} - {self.id}'

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

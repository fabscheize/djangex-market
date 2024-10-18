import re

from django.core import exceptions, validators
from django.db import models

from catalog.validators import ValidateContainsWords
from core.models import AbstractModel

PUNCTUATION_REGEX = re.compile(r'[\W_]')


def normalize_name(name):
    name = re.sub(PUNCTUATION_REGEX, '', name).lower()
    name = name.translate(str.maketrans('авекмнорстух', 'abekmhopctyx'))
    return name


class Category(AbstractModel):
    slug = models.CharField(
        verbose_name='слаг',
        max_length=200,
        validators=[
            validators.validate_slug,
        ],
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
        if Category.objects.filter(normalized_name=normalized).exists():
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
    slug = models.CharField(
        verbose_name='слаг',
        max_length=200,
        validators=[
            validators.validate_slug,
        ],
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
        if Tag.objects.filter(normalized_name=normalized).exists():
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

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

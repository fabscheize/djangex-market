import django.core.exceptions
import django.core.validators
import django.db

from catalog.validators import ValidateContainsWords
from core.models import AbstractModel


class Category(AbstractModel):
    slug = django.db.models.CharField(
        verbose_name='слаг',
        max_length=200,
        validators=[
            django.core.validators.validate_slug,
        ],
        unique=True,
        help_text=(
            'Только латинские буквы, цифры, знаки подчеркивания или дефиса'
        ),
    )
    weight = django.db.models.IntegerField(
        verbose_name='вес',
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Tag(AbstractModel):
    slug = django.db.models.CharField(
        verbose_name='слаг',
        max_length=200,
        validators=[
            django.core.validators.validate_slug,
        ],
        unique=True,
        help_text=(
            'Только латинские буквы, цифры, знаки подчеркивания или дефиса'
        ),
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Item(AbstractModel):

    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name='категория',
    )

    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name='теги',
    )

    text = django.db.models.TextField(
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

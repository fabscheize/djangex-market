import re

import django.core.exceptions
import django.core.validators
import django.db
import django.utils.deconstruct

from core.models import AbstractModel


@django.utils.deconstruct.deconstructible
class ValidateContainsWords(object):
    def __init__(self, *words):
        self.words = words
        self.pattern = re.compile(
            r'\b(' + '|'.join(re.escape(word) for word in words) + r')\b',
            re.IGNORECASE,
        )

    def __call__(self, text):
        if not self.pattern.search(text):
            raise django.core.exceptions.ValidationError(
                (
                    'Убедитесь, что в тесте есть одно из следующих слов: '
                    f'{", ".join(self.words)}'
                ),
                params={'text': text},
            )


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

# Generated by Django 4.2.16 on 2024-10-16 15:14

import catalog.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        primary_key=True,
                        serialize=False,
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                        verbose_name='id',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Максимум 150 символов',
                        max_length=150,
                        verbose_name='Название',
                    ),
                ),
                (
                    'is_published',
                    models.BooleanField(
                        default=True, verbose_name='Опубликовано'
                    ),
                ),
                (
                    'slug',
                    models.CharField(
                        help_text='Только латинские буквы, цифры, знаки подчеркивания или дефиса',
                        max_length=200,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile('^[-a-zA-Z0-9_]+\\Z'),
                                'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.',
                                'invalid',
                            )
                        ],
                        verbose_name='Слаг',
                    ),
                ),
                (
                    'weight',
                    models.IntegerField(
                        default=100,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(32767),
                        ],
                        verbose_name='Вес',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        primary_key=True,
                        serialize=False,
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                        verbose_name='id',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Максимум 150 символов',
                        max_length=150,
                        verbose_name='Название',
                    ),
                ),
                (
                    'is_published',
                    models.BooleanField(
                        default=True, verbose_name='Опубликовано'
                    ),
                ),
                (
                    'slug',
                    models.CharField(
                        help_text='Только латинские буквы, цифры, знаки подчеркивания или дефиса',
                        max_length=200,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile('^[-a-zA-Z0-9_]+\\Z'),
                                'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.',
                                'invalid',
                            )
                        ],
                        verbose_name='Слаг',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        primary_key=True,
                        serialize=False,
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                        verbose_name='id',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Максимум 150 символов',
                        max_length=150,
                        verbose_name='Название',
                    ),
                ),
                (
                    'is_published',
                    models.BooleanField(
                        default=True, verbose_name='Опубликовано'
                    ),
                ),
                (
                    'text',
                    models.TextField(
                        help_text='В описании обязательно должно быть слово "превосходно" или "роскошно"',
                        validators=[
                            catalog.models.ValidateContainsWords(
                                'превосходно', 'роскошно'
                            )
                        ],
                        verbose_name='Текст',
                    ),
                ),
                (
                    'categories',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='catalog.category',
                        verbose_name='Категория',
                    ),
                ),
                (
                    'tags',
                    models.ManyToManyField(
                        to='catalog.tag', verbose_name='Теги'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]

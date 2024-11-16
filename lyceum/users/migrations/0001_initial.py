# Generated by Django 4.2.16 on 2024-11-15 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('birthday', models.DateField(verbose_name='дата рождения')),
                (
                    'coffee_count',
                    models.IntegerField(
                        default=0, verbose_name='счетчик кофе'
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        default=None,
                        upload_to=users.models.Profile.avatar_directory_path,
                        verbose_name='аватар',
                    ),
                ),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='profile',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='пользователь',
                    ),
                ),
            ],
            options={
                'verbose_name': 'профиль пользователя',
                'verbose_name_plural': 'профили пользователей',
            },
        ),
    ]

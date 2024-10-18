# Generated by Django 4.2.16 on 2024-10-18 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='normalized_name',
            field=models.CharField(
                editable=False,
                max_length=150,
                unique=True,
                verbose_name='нормализованное имя',
            ),
        ),
        migrations.AddField(
            model_name='tag',
            name='normalized_name',
            field=models.CharField(
                editable=False,
                max_length=150,
                unique=True,
                verbose_name='нормализованное имя',
            ),
        ),
    ]

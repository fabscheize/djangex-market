# Generated by Django 4.2.16 on 2024-11-04 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_alter_category_name_alter_item_name_alter_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_published',
            field=models.BooleanField(
                default=True, verbose_name='опубликовано'
            ),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(
                help_text='Max 150 symbols',
                max_length=150,
                unique=True,
                verbose_name='название',
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='is_published',
            field=models.BooleanField(
                default=True, verbose_name='опубликовано'
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(
                help_text='Max 150 symbols',
                max_length=150,
                unique=True,
                verbose_name='название',
            ),
        ),
        migrations.AlterField(
            model_name='tag',
            name='is_published',
            field=models.BooleanField(
                default=True, verbose_name='опубликовано'
            ),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(
                help_text='Max 150 symbols',
                max_length=150,
                unique=True,
                verbose_name='название',
            ),
        ),
    ]

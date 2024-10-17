import django.core.validators
import django.db.models


class AbstractModel(django.db.models.Model):
    id = django.db.models.BigAutoField(
        verbose_name='id',
        primary_key=True,
        validators=[
            django.core.validators.MinValueValidator(1),
        ],
    )
    name = django.db.models.CharField(
        verbose_name='название',
        help_text='Максимум 150 символов',
        max_length=150,
        unique=True,
    )
    is_published = django.db.models.BooleanField(
        verbose_name='опубликовано',
        default=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        if len(self.name) <= 15:
            return self.name
        else:
            return self.name[:12] + '...'

import django.db.models
from django.utils.translation import gettext_lazy as _

__all__ = []


class Feedback(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name=_('имя'),
        max_length=100,
        blank=True,
        null=True,
    )
    mail = django.db.models.EmailField(
        verbose_name=_('почта'),
        max_length=100,
    )
    text = django.db.models.TextField(
        verbose_name=_('текст'),
    )
    created_on = django.db.models.DateTimeField(
        verbose_name=_('время создания'),
        auto_now_add=True,
        null=True,
    )

    class Meta:
        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')

    def __str__(self):
        return self.name if len(self.name) <= 21 else self.name[:18] + '...'

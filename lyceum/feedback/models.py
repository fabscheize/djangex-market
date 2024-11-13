from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = []


class Feedback(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', _('Новый')
        WIP = 'wip', _('В процессе')
        ANSWERED = 'ans', _('Отвечен')

    status = models.CharField(
        verbose_name=_('статус'),
        max_length=3,
        choices=Status.choices,
        default=Status.NEW,
    )
    name = models.CharField(
        verbose_name=_('имя'),
        max_length=100,
        blank=True,
        null=True,
    )
    mail = models.EmailField(
        verbose_name=_('почта'),
        max_length=100,
    )
    text = models.TextField(
        verbose_name=_('текст'),
    )
    created_on = models.DateTimeField(
        verbose_name=_('время создания'),
        auto_now_add=True,
        null=True,
    )

    class Meta:
        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')

    def __str__(self):
        return self.text if len(self.text) <= 21 else self.text[:18] + '...'


class StatusLog(models.Model):
    user = models.ForeignKey(
        verbose_name=_('пользователь'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    timestamp = models.DateTimeField(
        verbose_name=_('время'),
        auto_now_add=True,
    )
    feedback = models.ForeignKey(
        verbose_name=_('отзыв'),
        to=Feedback,
        on_delete=models.CASCADE,
        related_name='status_logs',
    )
    from_status = models.CharField(
        verbose_name=_('из статуса'),
        db_column='from',
        max_length=3,
    )
    to = models.CharField(
        verbose_name=_('в статус'),
        db_column='to',
        max_length=3,
    )

    class Meta:
        verbose_name = _('лог статуса')
        verbose_name_plural = _('логи статусов')

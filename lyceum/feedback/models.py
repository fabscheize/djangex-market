import uuid

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


class FeedbackAuthor(models.Model):
    feedback = models.OneToOneField(
        Feedback,
        related_name='author',
        on_delete=models.CASCADE,
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

    class Meta:
        verbose_name = _('автор отзыва')
        verbose_name_plural = _('авторы отзывов')


class FeedbackFile(models.Model):
    def feedback_directory_path(self, filename):
        return f'uploads/{self.feedback_id}/{uuid.uuid4()}-{filename}'

    feedback = models.ForeignKey(
        Feedback,
        related_name='files',
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        verbose_name=_('файл'),
        upload_to=feedback_directory_path,
        blank=True,
    )

    class Meta:
        verbose_name = _('прикрепленный файл')
        verbose_name_plural = _('прикрепленные файлы')


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

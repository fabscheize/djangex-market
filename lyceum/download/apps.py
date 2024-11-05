from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

__all__ = []


class DownloadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'download'
    verbose_name = _('Загрузка')

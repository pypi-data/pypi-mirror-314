from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class LogUiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logui'
    verbose_name = _('Logui')

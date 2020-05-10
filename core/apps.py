from django.apps import AppConfig
from django.utils.translation import ugettext as _


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = _("core")

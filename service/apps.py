from django.apps import AppConfig
from django.utils.translation import ugettext as _


class ServiceConfig(AppConfig):
    name = 'service'
    verbose_name = _("service")

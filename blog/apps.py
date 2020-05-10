from django.apps import AppConfig
from django.utils.translation import ugettext as _


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = _("core")

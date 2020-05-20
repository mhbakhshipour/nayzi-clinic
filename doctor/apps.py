from django.apps import AppConfig
from django.utils.translation import ugettext as _


class DoctorConfig(AppConfig):
    name = 'doctor'
    verbose_name = _("doctor")

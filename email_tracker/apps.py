from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EmailTrackerCenterConfig(AppConfig):
    name = 'email_tracker'
    verbose_name = _('Sent Emails')

#  flake8: noqa

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FeedConfig(AppConfig):
    name = 'apps.feed'
    verbose_name = _('Feed')

    def ready(self):
        pass

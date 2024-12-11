from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


__all__ = 'UTMConfig',


class UTMConfig(AppConfig):
    name = 'wcd_utm'
    verbose_name = pgettext_lazy('wcd_utm', 'UTM')

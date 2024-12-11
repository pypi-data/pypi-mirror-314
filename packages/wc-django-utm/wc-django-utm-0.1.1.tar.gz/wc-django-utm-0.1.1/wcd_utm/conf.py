from typing import *
from dataclasses import dataclass, field

from px_settings.contrib.django import settings as setting_wrap


__all__ = 'Settings', 'settings',


@setting_wrap('WCD_UTM')
@dataclass
class Settings:
    RESOLVABLE_PREFIXES: Sequence[str] = field(default_factory=lambda: ['utm_'])
    PARAMETERS: Sequence[str] = field(default_factory=lambda: [
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'utm_term',
        'utm_content',

        'gclid',  # Google ad click
        'aclk',  # Bing ad click
        'msclkid',  # MSFT ad click (non-Bing)
        'fbclid',  # Facebook ad click
        'twclid',  # Twitter ad click
    ])
    UNWRAP_PREFIXED_PARAMETERS: bool = False

    SESSION_STORAGE_KEY: str = 'utm_params_stored'
    SESSION_ACCESS_KEY: str = 'utm_params'

    HEADER_ORIGIN_URL: str = 'HTTP_X_UTM_ORIGIN_URL'
    HEADER_JSON: str = 'HTTP_X_UTM_JSON'


settings = Settings()

import os

from django.conf import settings

from kinder import config_parser as config


DEFAULT_CONFIG = {
    ('webservice', 'ORDER_REQUEST_FORCE_V3'): False,
}

conf = config.ProjectConfig(
    filenames=[
        os.path.normpath(
            os.path.join(settings.CONFIG_PATH, 'concentrator.conf'))
    ],
    defaults=DEFAULT_CONFIG
)

ORDER_REQUEST_FORCE_V3 = conf.get_bool(
    'webservice', 'ORDER_REQUEST_FORCE_V3', False)

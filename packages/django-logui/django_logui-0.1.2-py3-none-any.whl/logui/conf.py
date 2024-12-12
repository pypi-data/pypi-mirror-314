# conf.py
from django.conf import settings


def get_setting(name, default=None, required=False):
    value = getattr(settings, name, None)
    if value is None:
        if required:
            if default is not None:
                return default
            raise ValueError(f'Missing required django setting: {name}')
        return default
    return value


LOGS_DIR = get_setting('LOGS_DIR', required=True)
LOGUI_REQUEST_RESPONSE_LOGGER_NAME = get_setting('LOGUI_REQUEST_RESPONSE_LOGGER_NAME')
LOGUI_URL_PREFIX = get_setting('LOGUI_URL_PREFIX', 'logui/')
LOGUI_CONTROLLERS_SETTINGS = get_setting('LOGUI_CONTROLLERS_SETTINGS', {
    'auth_required': True,
    'log_name': False,
    'not_auth_redirect': f'/admin/login/?next=/{get_setting("LOGUI_URL_PREFIX", "logui/")}'
}, required=True)

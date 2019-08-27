from .base_settings import *

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'webpack_loader',
    'foodalert',
    'rest_framework',
    'phonenumber_field',
    'dbmail',
    'premailer',
    'django.contrib.sites'
]

SITE_ID = 1

if os.getenv("ENV") == "localdev":
    DEBUG = True
else:
    DEBUG = False


WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'foodalert/bundles/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR,
                                   'foodalert',
                                   'static',
                                   'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default=" ")


# SETTING FOR WHICH SMS TO USE
FOODALERT_USE_SMS = 'twilio'

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "NONE")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "NONE")
TWILIO_NOTIFY_SERVICE_ID = os.getenv("TWILIO_NOTIFY_SERVICE_ID", "NONE")

FOODALERT_AUTHZ_GROUPS = {
    'create': 'u_test_host',
    'audit': 'u_test_admin'
}


if os.getenv("AUTH", "NONE") == "SAML_MOCK":
    MOCK_SAML_ATTRIBUTES['isMemberOf'] = ['u_test_host', 'u_test_admin']
    from django.urls import reverse_lazy
    LOGIN_URL = reverse_lazy('saml_login')
    LOGOUT_URL = reverse_lazy('saml_logout')

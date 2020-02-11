from .base_settings import *
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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

LOGGING['handlers']['file'] = {
    'level':'INFO',
    'class':'logging.FileHandler',
    'filename':'/app/foodalert.log',
}

LOGGING['loggers'][''] = {
    'handlers': ['file'],
    'level': 'DEBUG'
}

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default=" ")

# SETTING FOR WHICH SMS TO USE
FOODALERT_USE_SMS = 'twilio'

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "NONE")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "NONE")
TWILIO_NOTIFY_SERVICE_ID = os.getenv("TWILIO_NOTIFY_SERVICE_ID", "NONE")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "NONE")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "NONE")
AWS_MESSAGE_ATTRIBUTES = {
    'SMSType': 'Promotional',
    'MaxPrice': '0.50',
    'mySenderID': 'foodalert'
}

# SETTINGS FOR EMAIL BACKEND
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST = 'localhost'
else:
    SAFE_EMAIL_RECIPIENT = os.getenv("SAFE_EMAIL_RECIPIENT")
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

FOODALERT_AUTHZ_GROUPS = {
    'create': os.getenv("FA_HOST_GROUP", 'u_test_host'),
    'audit': os.getenv("FA_AUDIT_GROUP", 'u_test_admin')
}

if os.getenv("AUTH", "NONE") == "SAML_MOCK":
    MOCK_SAML_ATTRIBUTES['isMemberOf'] = [
        FOODALERT_AUTHZ_GROUPS['create'],
        FOODALERT_AUTHZ_GROUPS['audit']
    ]


DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES
}

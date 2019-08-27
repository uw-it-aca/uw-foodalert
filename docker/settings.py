from .base_settings import *

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'webpack_loader',
    'foodalert',
    'rest_framework',
    'phonenumber_field',
    'dbmail',
    'premailer',
    'django.contrib.sites',
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'prereq_map/bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'prereq_map', 'static', 'webpack-stats.json'),
    }
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

DATA_ROOT = os.path.join(BASE_DIR, "prereq_map/data")

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default=" ")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'debug':  True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'prereq_map.context_processors.google_analytics',
                'prereq_map.context_processors.django_debug',
            ],
        }
    }
]

if os.getenv("ENV") == "localdev":
    DEBUG = True

if os.getenv("AUTH", "NONE") == "SAML_MOCK":
    MOCK_SAML_ATTRIBUTES['isMemberOf'] = ['u_test_host', 'u_test_admin']

# SETTING FOR WHICH SMS TO USE
FOODALERT_USE_SMS = 'twilio'

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "NONE")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "NONE")
TWILIO_NOTIFY_SERVICE_ID = os.getenv("TWILIO_NOTIFY_SERVICE_ID", "NONE")

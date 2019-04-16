import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.getenv('DJANGO_SECRET', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'foodalert',
    'rest_framework',
    'dbmail',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

USE_TZ = True

ROOT_URLCONF = 'travis.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travis_ci_test',
        'USER': 'travis',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    }
]

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

TWILIO_ACCOUNT_SID = "XXX"
TWILIO_AUTH_TOKEN = "XXX"
TWILIO_NOTIFY_SERVICE_ID = "XXX"
TWILIO_FROM = ''

MOCK_SAML_ATTRIBUTES = {}
MOCK_SAML_ATTRIBUTES['isMemberOf'] = ['u_test_host', 'u_test_admin']

FOODALERT_AUTHZ_GROUPS = {
    'create': 'u_test_host',
    'audit': 'u_test_admin'
}

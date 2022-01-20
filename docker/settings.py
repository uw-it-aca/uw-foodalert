from .base_settings import *
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

INSTALLED_APPS += [
    "webpack_loader",
    "foodalert",
    "rest_framework",
    "phonenumber_field",
    "dbmail",
    "premailer",
    "django.contrib.sites",
    "django_dbq"
]

SITE_ID = 1

if os.getenv("ENV") == "localdev":
    DEBUG = True
else:
    DEBUG = False

JOBS = {
    "queue_messages": {
        "tasks": ["foodalert.jobs.queue_messages"],
    },
    "send_email": {
        "tasks": ["foodalert.jobs.send_email"],
    },
    "send_sms": {
        "tasks": ["foodalert.jobs.send_sms"],
    },
}

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "foodalert/bundles/",  # must end with slash
        "STATS_FILE": os.path.join(
            BASE_DIR, "foodalert", "static", "webpack-stats.json"
        ),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default=" ")

# SETTING TWILIO SMS
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "NONE")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "NONE")
TWILIO_NOTIFY_SERVICE_ID = os.getenv("TWILIO_NOTIFY_SERVICE_ID", "NONE")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "NONE")

# SETTINGS FOR EMAIL BACKEND
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_HOST = "localhost"
else:
    # SAFE_EMAIL_RECIPIENT = os.getenv("SAFE_EMAIL_RECIPIENT")
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
    EMAIL_SSL_CERTFILE = os.getenv("CERT_PATH", "")
    EMAIL_SSL_KEYFILE = os.getenv("KEY_PATH", "")

FOODALERT_AUTHZ_GROUPS = {
    "create": os.getenv("FA_HOST_GROUP", "u_test_host"),
    "audit": os.getenv("FA_AUDIT_GROUP", "u_test_admin"),
}

if os.getenv("AUTH", "NONE") == "SAML_MOCK":
    MOCK_SAML_ATTRIBUTES["isMemberOf"] = [
        FOODALERT_AUTHZ_GROUPS["create"],
        FOODALERT_AUTHZ_GROUPS["audit"],
    ]


DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        "rest_framework.renderers.BrowsableAPIRenderer",
    )

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
}

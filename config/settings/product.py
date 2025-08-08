from datetime import timedelta
from .base_settings import *


CSRF_TRUSTED_ORIGINS = ['https://*.up.railway.app',
                        "https://smart-room-production.up.railway.app/",
                        'https://smart.farukseker.com.tr'
                        'https://smart.farukseker.com.tr/',
                        'https://smartapp.farukseker.com.tr/',
                        'https://smartapp.farukseker.com.tr',
                        'https://24m9nvnv.up.railway.app',
                        ]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': env('PGDATABASE'),
        'USER': env('PGUSER'),
        'PASSWORD': env('PGPASSWORD'),
        'HOST': env('PGHOST'),
        'PORT': env('PGPORT')
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env('REDIS_CHANEL_URL')],
            "symmetric_encryption_keys": [SECRET_KEY],
        },
    }
}


## log

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[DjangoIntegration(),],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


LOGIN_URL = 'admin/login'
LOGIN_REDIRECT_URL = '/'

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [
#     'https://smart.farukseker.com.tr/',
#     'https://smart.farukseker.gen.tr/',
#     'https://chipper-beijinho-7e220b.netlify.app/'
# ]

SIMPLE_JWT: dict = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=15),
}
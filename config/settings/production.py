from config.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sahibmoney',
        'USER': 'django',
        'PASSWORD': 'ddd836a86c65b57c439728991489f341',
        'HOST': 'localhost',
        'PORT': '',
    }
}

APP_SUPPORT_EMAIL = "support@sahibmoney.com"
APP_ADMIN_EMAIL = "admin@sahibmoney.com"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.privateemail.com'
EMAIL_HOST_USER = APP_SUPPORT_EMAIL
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = APP_SUPPORT_EMAIL

SITE_BASE_URL = "http://sahibmoney.com"

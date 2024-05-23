import os
import sys
from pathlib import Path
import dj_database_url
import cloudinary


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "yh8w0vp&u@yh2z@q8elg44bsx#ze18(pqrn#ojah9pn@kb(qp8"

DEBUG = (sys.argv[1] == 'runserver')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'ajax_select',
    'bootstrapform',
    'cloudinary',
    'simple_email_confirmation',
    'font_awesome',
    'gamestore',
    'api',
    'django_social_share',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'diploma2024.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'diploma2024.wsgi.application'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = (sys.argv[1] != 'runserver')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'django-reinhardt.herokuapp.com']

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

MEDIAFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'media'),
]

cloudinary.config(
  cloud_name="dzoczhaes",
  api_key="888892614347162",
  api_secret="dAib0A3BEzedwhW5IggWoPuKDIA"
)

LOGIN_REDIRECT_URL = "/"
AUTH_USER_MODEL = 'gamestore.User'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seedgamestore1@outlook.com' 
EMAIL_HOST_PASSWORD = 'Diploma2024$'
DEFAULT_FROM_EMAIL = 'seedgamestore1@outlook.com'

SITE_ID = 5

AJAX_SELECT_BOOTSTRAP = False

STRIPE_PUBLIC_KEY = 'pk_test_51PFaOr02IzE0WCScMA1I8v2wek3qjdM3Il6rLE4IxkHT0dBLbWqZUjaPa1A9ZjR3Svtezgt0vFCSW8OoQZi7rYGq00U2dmWFTJ'
STRIPE_SECRET_KEY = 'sk_test_51PFaOr02IzE0WCScZP8sMoIAdWGkPIYUHN1iqBTRI5llhTfLKew7vaK6Xw9U4j8wSRe90tWOycn720YPQXLev6BF00Yf4h57T9'
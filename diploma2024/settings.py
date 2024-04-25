"""
Django settings for wsd2018project project on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/5.0.4/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0.4/ref/settings/
"""

import os
import sys
import platform
from pathlib import Path
import dj_database_url
import django_heroku
import cloudinary

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0.4/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# this is same for everyone – you should probably alter it!
SECRET_KEY = "yh8w0vp&u@yh2z@q8elg44bsx#ze18(pqrn#ojah9pn@kb(qp8"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (sys.argv[1] == 'runserver')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'ajax_select',
    'bootstrapform',
    'cloudinary',
    'simple_email_confirmation',
    'social_django',
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
    'social_django.middleware.SocialAuthExceptionMiddleware'
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


# Database
# https://docs.djangoproject.com/en/5.0.4/ref/settings/#databases


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

# Internationalization
# https://docs.djangoproject.com/en/5.0.4/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Rerdirect all traffic to HTTPS on server
SECURE_SSL_REDIRECT = (sys.argv[1] != 'runserver')

# Allow all host headers
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'django-reinhardt.herokuapp.com']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0.4/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

MEDIAFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'media'),
]

# Cloudinary configs (For media uploads)
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
EMAIL_HOST_USER = 'seedgamestore@outlook.com' 
EMAIL_HOST_PASSWORD = 'Diploma2024$'
DEFAULT_FROM_EMAIL = 'seedgamestore@outlook.com'

SITE_ID = 5

# django-ajax-selects settings
AJAX_SELECT_BOOTSTRAP = False

# Activate Django-Heroku.
django_heroku.settings(locals())
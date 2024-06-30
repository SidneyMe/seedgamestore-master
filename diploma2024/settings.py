import os
import sys
from pathlib import Path
import dj_database_url
import platform
import cloudinary
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set CSRF cookie settings
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Define the base directory and project root
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Get the secret key from environment variable
SECRET_KEY = os.getenv('SECRET_KEY')

# Set debug mode based on command line argument
DEBUG = (sys.argv[1] == 'runserver')

# Set the default auto field for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# List of installed apps
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
    'django_select2',
]

# List of middleware classes
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

# Root URL configuration
ROOT_URLCONF = 'diploma2024.urls'

# Template settings
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

# WSGI application
WSGI_APPLICATION = 'diploma2024.wsgi.application'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MySQL80',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Override for Doker
if os.getenv('RUNNING_IN_DOCKER') == 'True':
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

# Password validation settings
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

# Language settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# X-Frame-Options header settings
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Cross-site sharing allowed methods
XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

# Update DATABASES settings if DATABASE_URL environment variable is present
if 'DATABASE_URL' in os.environ:
    DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

# Secure proxy SSL header settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Secure SSL redirect settings
SECURE_SSL_REDIRECT = (sys.argv[1] != 'runserver')

# Allowed hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'seedgamestore.up.railway.app', '0.0.0.0']

# Static files settings
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files settings
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

MEDIAFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'media'),
]

# Cloudinary configuration
cloudinary.config(
  cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
  api_key=os.getenv("CLOUDINARY_API_KEY"),
  api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Login redirect URL
LOGIN_REDIRECT_URL = "/"

# Custom user model
AUTH_USER_MODEL = 'gamestore.User'

# Email backend settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')

SITE_ID = 5

AJAX_SELECT_BOOTSTRAP = False

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
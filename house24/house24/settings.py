"""
Django settings for house24 project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

try:
    from house24.config import db_name, db_password, db_user
except ModuleNotFoundError:
    db_name = 'db_name'
    db_password = 'db_password'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'changekey')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG', 1))

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', None)
ALLOWED_HOSTS = ALLOWED_HOSTS.split(" ") if ALLOWED_HOSTS else ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'rest_framework',
    'db',
    'website',
    'rest_api',
    'admin_panel',
    'user_profile',
    'robots',
    'axes',
    'health_check',
    'health_check.cache',
    'health_check.storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'admin_panel.middleware.AdminSessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',

    'admin_panel.middleware.AdminCheckMiddleware',
    'user_profile.middleware.CheckUserProfileAccess',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'house24.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['media/file_templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'admin_panel.context_processors.add_new_users_to_template',
                'admin_panel.context_processors.add_unread_messages_to_template',
                'user_profile.context_processors.add_client_info_to_template'
            ],
        },
    },
]

WSGI_APPLICATION = 'house24.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('POSTGRES_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('POSTGRES_DB', db_name),
        'USER': os.environ.get('POSTGRES_USER', db_user),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', db_password), # temporary user and password. Doesnt important absolutely
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432')
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
AUTHENTICATION_BACKENDS = ['axes.backends.AxesBackend',
                           'website.auth_backend.EmailBackend',
                           'website.auth_backend.IDBackend']

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-EN'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = Path(__file__).parent.parent.joinpath('static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = Path(__file__).parent.parent.joinpath('media/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'db.User'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'djangokinoteatrmail@gmail.com'  # This is a test account without any important data
EMAIL_HOST_PASSWORD = 'Do24hfjzbe23h'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SITE_ID = 1
ROBOTS_SITEMAP_URLS = [
    'http://127.0.0.1/sitemap.xml',
]

SOCKET_IO_PATH = os.environ.get('SOCKET_IO_PATH', 'http://127.0.0.1:5000/')

CSP_SCRIPT_SRC = ('unsafe-inline', 'unsafe-eval')
CSP_IMG_SRC = ('unsafe-inline',)
CSP_FONT_SRC = ('unsafe-inline',)
CSP_STYLE_SRC = ('unsafe-inline',)
CSP_DEFAULT_SRC = ("'none'",)

SECURE_REFERRER_POLICY = 'same-origin'

EXTRA_CHECKS = {
    'checks': [
        # Forbid `unique_together`:
        'no-unique-together',
        # Require non empty `upload_to` argument:
        'field-file-upload-to',
        # Use the indexes option instead:
        'no-index-together',
        # Each model must be registered in admin:
        'model-admin',
        # FileField/ImageField must have non empty `upload_to` argument:
        'field-file-upload-to',
        # Text fields shouldn't use `null=True`:
        'field-text-null',
        # Prefer using BooleanField(null=True) instead of NullBooleanField:
        'field-boolean-null',
        # Don't pass `null=False` to model fields (this is django default)
        'field-null',
        # ForeignKey fields must specify db_index explicitly if used in
        # other indexes:
        {'id': 'field-foreign-key-db-index', 'when': 'indexes'},
        # If field nullable `(null=True)`,
        # then default=None argument is redundant and should be removed:
        'field-default-null',
        # Fields with choices must have companion CheckConstraint
        # to enforce choices on database level
        'field-choices-constraint',
    ],
}

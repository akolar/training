"""
Django settings for training project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

SECRET_KEY = os.environ['SECRET_KEY']

OPENSHIFT = 'OPENSHIFT_NAMESPACE' in os.environ
DEBUG = (os.environ.get('DEBUG', '0') == '1') or not OPENSHIFT
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'training.akolar.com'
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'training.urls'
WSGI_APPLICATION = 'training.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'training',
        'USER': (os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
                 if OPENSHIFT else os.environ['PSQL_USER']),
        'PASSWORD': (os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']
                     if OPENSHIFT else os.environ['PSQL_PASSWD']),
        'HOST': (os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
                 if OPENSHIFT else ''),
        'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'] if OPENSHIFT else ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

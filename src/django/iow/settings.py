"""
Django settings for iow project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#TODO: move this to .env

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "secret")

ENVIRONMENT = os.getenv("DJANGO_ENV", "Development")
VALID_ENVIRONMENTS = ("Production", "Staging", "Development")
if ENVIRONMENT not in VALID_ENVIRONMENTS:
    raise ImproperlyConfigured(
        "Invalid ENVIRONMENT provided, must be one of {}".format(VALID_ENVIRONMENTS)
    )

LOGLEVEL = os.getenv("DJANGO_LOG_LEVEL", "INFO")

GIT_COMMIT = os.getenv("GIT_COMMIT", "UNKNOWN")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENVIRONMENT == "Development"

ALLOWED_HOSTS = [
    "localhost",
]

if ENVIRONMENT == "Development":
    # Services within the bridge network access Django by resolving its
    # container name. Also, some folks develop on remote workstations.
    ALLOWED_HOSTS.extend(os.getenv("DJANGO_ALLOWED_HOSTS", "localhost").split(","))

if ENVIRONMENT in ["Production", "Staging"]:
    # The Elastic Load Balancer HTTP health check will use the target
    # instance's private IP address for the Host header.
    #
    # The following steps look up the current instance's private IP address
    # (via the ECS container metadata URI) and add it to the Django
    # ALLOWED_HOSTS configuration so that health checks pass.
    response = requests.get(os.getenv("ECS_CONTAINER_METADATA_URI"))
    if response.ok:
        container = response.json()
        for network in container["Networks"]:
            for addr in network["IPv4Addresses"]:
                ALLOWED_HOSTS.append(addr)
    else:
        raise ImproperlyConfigured("Unable to fetch instance metadata")

    # Ensure that Django can service requests originating from our public hosted
    # zone.
    R53_PUBLIC_HOSTED_ZONE = os.getenv("R53_PUBLIC_HOSTED_ZONE")
    if R53_PUBLIC_HOSTED_ZONE == None:
        raise ImproperlyConfigured("Empty R53_PUBLIC_HOSTED_ZONE provided")
    ALLOWED_HOSTS.append(".{}".format(os.getenv("R53_PUBLIC_HOSTED_ZONE")))

    # Ensure Django knows to determine whether an inbound request was made over
    # HTTPS by the ALB's HTTP_X_FORWARDED_PROTO header.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # Session Security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    "django.contrib.gis",
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles',
    'django_extensions',
    "rest_framework",
    "rest_framework_gis",
    'watchman',
    "ecsmanage",
    "api",
    "simple_history",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "spa.middleware.SPAMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "simple_history.middleware.HistoryRequestMiddleware",
]

# Web security settings (match Terraform Cloudfront Header Response Policy)
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 63072000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Session security
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 7200  # 2 hours in seconds, client-suggested

ROOT_URLCONF = 'iow.urls'

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
        },
    },
]

WSGI_APPLICATION = 'iow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
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

# Logging
# https://docs.djangoproject.com/en/3.2/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = ((os.path.join(STATIC_ROOT, "static")),)

# From the django-spa README
# https://github.com/metakermit/django-spa/tree/418fd20e0cf1339ac259d16ce3d6f78c2868d1cd

STATICFILES_STORAGE = "spa.storage.SPAStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Watchman
# https://github.com/mwarkentin/django-watchman

WATCHMAN_ERROR_CODE = 503
WATCHMAN_CHECKS = ('watchman.checks.databases',)


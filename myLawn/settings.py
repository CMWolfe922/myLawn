"""
Django settings for myLawn project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4fydjl@y=hon2-i_phsz9gmw5djw#_*l0=x)oor=!x)f097k4i"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
GDAL_LIBRARY_PATH = "C:\\OSGeo4W\\bin\\gdal306.dll"  #os.environ.get('GDAL_306_PATH') or os.environ.get('GDAL_LIBRARY_PATH') or os.environ.get('GDAL_SPATIALITE_PATH') or os.environ.get('GDAL_PLUGINS') or os.environ.get("GDAL_BATCH")

INSTALLED_APPS = [
    # Other installed apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.sites',
    
    'accounts.apps.AccountsConfig',
    "lawn_manager.apps.LawnManagerConfig",
    
    # Used Apps
    # "crispy_forms",
    # "crispy_bootstrap5",
    # "django_extensions",
    # "django_filters",
    # "imagekit",
    
    # Rest Framework Apps
    # "rest_framework",
    # "rest_framework.authtoken",
    # "rest_framework_gis",
    # "rest_framework_swagger",
    # "rest_framework_simplejwt",
    # "rest_framework_simplejwt.token_blacklist",
    # "rest_framework_simplejwt.token_blacklist.models",
    # "rest_framework_simplejwt.token_blacklist.admin",
    # "rest_framework_simplejwt.token_blacklist.serializers",
    # "rest_framework_simplejwt.token_blacklist.views",
    # "rest_framework_simplejwt.token_blacklist.urls",
    # "rest_framework_simplejwt.token_blacklist.management",
    # "rest_framework_simplejwt.token_blacklist.management.commands",
    # "rest_framework_simplejwt.token_blacklist.signals",

    # Third party apps
    "django_cleanup",
    
]



MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "myLawn.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "myLawn.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "MyLawn.db",
    },
    "gis_db": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": "mylawngis.db",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Chicago"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = BASE_DIR / "static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# CRISPY FORMS SETTINGS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# IMAGEKIT SETTINGS
IMAGEKIT_CACHEFILE_DIR = "cache"
IMAGEKIT_CACHEFILE_BACKEND = "imagekit.cachefiles.backends.Simple"
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = "imagekit.cachefiles.strategies.Optimistic"
IMAGEKIT_DEFAULT_CACHEFILE_BACKEND = "imagekit.cachefiles.backends.Simple"

# DJANGO EXTENSIONS SETTINGS
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True

# DJANGO FILTERS SETTINGS
DJANGO_FILTERS_HELP_TEXT_FILTER = False



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.NewUser"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


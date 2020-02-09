"""
Django settings for nwapp project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import logging.config
import datetime
import os
import environ
import re
import sys
from django.urls import reverse_lazy

'''
django-environ
https://github.com/joke2k/django-environ
'''
root = environ.Path(__file__) - 3 # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False),) # set default values and casting
environ.Env.read_env() # reading .env file

SITE_ROOT = root()


'''
django
https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
'''

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY') # Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ

# SECURITY WARNING: Do not run true in production environment.
DEBUG = env('DEBUG', default=False)
TEMPLATE_DEBUG = env('DEBUG', default=False)

ALLOWED_HOSTS = ['*']

SITE_ID = 1
ADMIN_ENABLED = False

# Application definition

# This configuration ensures that all authenticated users from the public
# schema to exist authenticated in the tenant schemas as well. This is
# important to have "django-tenants" work
SESSION_COOKIE_DOMAIN = '.' + env("NWAPP_BACKEND_HTTP_DOMAIN")

# This configuration ensures all authentication enforcement redirects to this
# specific URL in our application.
LOGIN_URL="/login/"


# Application definition

SHARED_APPS = ( # (Django-Tenants)
    # Third Party Apps
    'django_tenants',
    'rest_framework',
    'django_filters',
    'django_rq',
    'redis_cache',
    'corsheaders',
    'oauth2_provider',
    'djmoney',
    # 'anymail',
    # 'phonenumber_field',
    'storages',
    'sorl.thumbnail',
    # . . .

    # Our Apps
    'shared_foundation.apps.SharedFoundationConfig',
    'shared_gateway.apps.SharedGatewayConfig',
    'shared_organization.apps.SharedOrganizationConfig',

    # Django Apps
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Extra Django Apps
    'django.contrib.postgres',   # Postgres full-text search: https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/search/
    'django.contrib.gis',        # Geo-Django: https://docs.djangoproject.com/en/dev/ref/contrib/gis/
    'django.contrib.humanize',   # Humanize: https://docs.djangoproject.com/en/dev/ref/contrib/humanize/
)

TENANT_APPS = ( # (Django-Tenants)
    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.contenttypes',

    # Our Apps
    'tenant_foundation.apps.TenantFoundationConfig',
    'tenant_dashboard.apps.TenantDashboardConfig',
    'tenant_member.apps.TenantMemberConfig',
    'tenant_area_coordinator.apps.TenantAreaCoordinatorConfig',
    'tenant_private_file_upload.apps.TenantPrivateFileUploadConfig',
    'tenant_private_image_upload.apps.TenantPrivateImageUploadConfig',
    'tenant_associate.apps.TenantAssociateConfig',
    'tenant_staff.apps.TenantStaffConfig',
    'tenant_watch.apps.TenantWatchConfig',
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS] # (Django-Tenants)

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',                    # Third Party
    'django_tenants.middleware.main.TenantMainMiddleware',      # Third Party
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',      # Extra Django App
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shared_foundation.middleware.ip_middleware.IPMiddleware',  # Custom App
    'django.middleware.locale.LocaleMiddleware',                # Extra Django App
    'oauth2_provider.middleware.OAuth2TokenMiddleware',         # Third Party
]

ROOT_URLCONF = 'nwapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',    # Extra Django App
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'foundation.context_processors.constants',          # Custom App
                # 'social_django.context_processors.backends',        # Extra Django App
                # 'social_django.context_processors.login_redirect',  # Extra Django App
            ],
        },
    },
]

WSGI_APPLICATION = 'nwapp.wsgi.application'


'''
Django-Tenants
https://github.com/tomturner/django-tenants
'''

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

ORIGINAL_BACKEND = "django.contrib.gis.db.backends.postgis"

TENANT_MODEL = "shared_foundation.SharedOrganization"

TENANT_DOMAIN_MODEL = "shared_foundation.SharedOrganizationDomain"


'''
Database
https://docs.djangoproject.com/en/2.2/ref/settings/#databases
'''

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend', # (Django-Tenants)
        'CONN_MAX_AGE': 0,
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}


'''
Password validation
https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
'''

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


'''
Password hashers
https://docs.djangoproject.com/en/2.2/topics/auth/passwords/
'''

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher', # Note: https://argon2-cffi.readthedocs.io/en/stable/
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]


"""
Custom authentication
https://docs.djangoproject.com/en/dev/topics/auth/customizing/
"""

AUTH_USER_MODEL = 'shared_foundation.SharedUser'

AUTHENTICATION_BACKENDS = [
    # Custom authentication.
    'shared_foundation.backends.NWAppEmailPasswordAuthenticationBackend',
    'shared_foundation.backends.NWAppPasswordlessAuthenticationBackend',

    # oAuth 2.0 authentication.
    'oauth2_provider.backends.OAuth2Backend',
]


'''
Internationalization
https://docs.djangoproject.com/en/2.2/topics/i18n/
'''

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ugettext = lambda s: s
LANGUAGES = (
    ('en', ugettext('English')),
#    ('fr', ugettext('French')),
#    ('es', ugettext('Spanish')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)


"""
Email
https://docs.djangoproject.com/en/1.11/topics/email/
"""

EMAIL_BACKEND = env("EMAIL_BACKEND")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
DEFAULT_TO_EMAIL = env("DEFAULT_TO_EMAIL")


"""
Anymail
https://github.com/anymail/django-anymail
"""

ANYMAIL = {
    # (exact settings here depend on your ESP...)
    "MAILGUN_API_KEY": env("MAILGUN_ACCESS_KEY"),
    "MAILGUN_SENDER_DOMAIN": env("MAILGUN_SERVER_NAME"),
}


'''
################################################################################
# OLD CONFIGURATION
# THIS IS THE PREVIOUS CONFIGURATION WE HAVE USED WHEN WE WERE USING THE
# AMAZON AWS S3 SERVICES.
################################################################################
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
'''


'''
django-storages
https://github.com/jschneier/django-storages
'''

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_STATIC_LOCATION = 'static'
AWS_DEFAULT_ACL = 'private'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
AWS_LOCATION = 'static'
STATIC_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
DEFAULT_FILE_STORAGE = 'nwapp.s3utils.PublicMediaStorage'

AWS_PRIVATE_MEDIA_LOCATION = 'media/private'
PRIVATE_FILE_STORAGE = 'nwapp.s3utils.PrivateMediaStorage'


'''
Template Directory
'''

TEMPLATE_DIRS = (
    BASE_DIR + '/templates/',
)


'''
django-cors-headers
https://github.com/ottoyiu/django-cors-headers
'''

CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-disposition',
    'accept-encoding',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)


"""
Error Emailing
https://docs.djangoproject.com/en/dev/topics/logging/
"""

# Disable Django's logging setup
LOGGING_CONFIG = None

LOGLEVEL = env("NWAPP_LOGLEVEL")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


"""
Error Reporting
https://docs.djangoproject.com/en/2.2/howto/error-reporting/
"""

IGNORABLE_404_URLS = [
    re.compile(r'^$'),
    re.compile(r'^/$'),
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin/'),
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
]


'''
django-oauth-toolkit
https://github.com/jazzband/django-oauth-toolkit
'''

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'introspection': 'Access to introspect resource'
    }
}
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'
OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = 'oauth2_provider.AccessToken'


'''
Django-REST-Framework
https://github.com/encode/django-rest-framework
'''

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'shared_foundation.drf.permissions.DisableOptionsPermission',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_msgpack.renderers.MessagePackRenderer',  # Third-party library.
        # 'rest_framework.renderers.BrowsableAPIRenderer'  # Not to be used in prod.
    ],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework_msgpack.parsers.MessagePackParser',  # Third-party library.
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'shared_foundation.drf.pagination.NWAppResultsSetPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10
}


"""
django-rq
https://github.com/rq/django-rq
"""

RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'default',
    }
}


"""
django-redis-cache
https://github.com/sebleier/django-redis-cache
"""

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'KEY_FUNCTION': 'django_tenants.cache.make_key', # (Django-Tenants)
        'REVERSE_KEY_FUNCTION': 'django_tenants.cache.reverse_key', # (Django-Tenants)
    },
}

# SESSION_ENGINE = 'redis_sessions.session'


"""
django-redis-sessions
https://github.com/martinrusev/django-redis-sessions
"""

SESSION_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'prefix': 'session',
    'socket_timeout': 1
}


'''
sorl-thumbnail
https://github.com/jazzband/sorl-thumbnail
'''

THUMBNAIL_ENGINE = 'nwapp.snorlutil.Engine'
THUMBNAIL_DEBUG = env('DEBUG', default=False)
THUMBNAIL_FORCE_OVERWRITE = True


'''
Application Specific Variables
https://github.com/nwapp/nwapp-back
'''

NWAPP_BACKEND_HTTP_PROTOCOL = env("NWAPP_BACKEND_HTTP_PROTOCOL")
NWAPP_BACKEND_HTTP_DOMAIN = env("NWAPP_BACKEND_HTTP_DOMAIN")
# NWAPP_BACKEND_DEFAULT_MONEY_CURRENCY = env("NWAPP_BACKEND_DEFAULT_MONEY_CURRENCY")
NWAPP_RESOURCE_SERVER_NAME = env("NWAPP_RESOURCE_SERVER_NAME")
# NWAPP_RESOURCE_SERVER_INTROSPECTION_URL = env("NWAPP_RESOURCE_SERVER_INTROSPECTION_URL")
# NWAPP_RESOURCE_SERVER_INTROSPECTION_TOKEN = env("NWAPP_RESOURCE_SERVER_INTROSPECTION_TOKEN")
# NWAPP_FRONTEND_HTTP_PROTOCOL = env("NWAPP_FRONTEND_HTTP_PROTOCOL")
# NWAPP_FRONTEND_HTTP_DOMAIN = env("NWAPP_FRONTEND_HTTP_DOMAIN")


'''
Django Custom Settings Override
https://docs.djangoproject.com/en/dev/ref/settings/
'''

# Note:
# (1) 2.5 MB x 20 = 50 MB
# (2) https://docs.djangoproject.com/en/dev/ref/settings/#data-upload-max-memory-size
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440 * 20

"""
Django settings for TiBillet project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
# noinspection DjangoDebugModeSettings
if os.environ.get('DEBUG_DJANGO') == "True":
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ['*']
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# Application definition

CORS_ORIGIN_WHITELIST = [
    'http://localhost',
    'http://localhost:3000',
    'http://localhost:3001',
    'http://django-local.org:3000',
    'http://demo.django-local.org:3000',
    'http://demo.django-local.org',
]

SHARED_APPS = (
    'django_tenants',  # mandatory
    # 'jet.dashboard',
    # 'jet',
    'Customers',  # you must list the app where your tenant model resides in

    'django.contrib.contenttypes',

    # everything below here is optional
    'django.contrib.auth',
    'AuthBillet',
    'QrcodeCashless',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    # "allauth.socialaccount.providers.github",

    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'channels',
    'django_extensions',
    'Administration',
    'MetaBillet',
    'root_billet',

    'solo',
    'stdimage',
    'corsheaders',
)

# CodeLogin_app/settings.py
TENANT_COLOR_ADMIN_APPS = False

TENANT_APPS = (
    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.contenttypes',
    'rest_framework_api_key',
    # your tenant-specific apps
    'BaseBillet',
    'ApiBillet',
    'PaiementStripe',
    'wsocket',
    'tibrss',

)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]
TENANT_MODEL = "Customers.Client"  # app.Model
TENANT_DOMAIN_MODEL = "Customers.Domain"  # app.Model
ROOT_URLCONF = 'TiBillet.urls_tenants'
PUBLIC_SCHEMA_URLCONF = 'TiBillet.urls_public'
SITE_ID = 1
AUTH_USER_MODEL = 'AuthBillet.TibilletUser'

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

WSGI_APPLICATION = 'TiBillet.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',  # Add 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework_api_key.permissions.HasAPIKey",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    #     'REFRESH_TOKEN_LIFETIME': timedelta(seconds=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


# DJOSER = {
#     "SEND_ACTIVATION_EMAIL": True,
#     "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
#     "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
#     "USERNAME_RESET_CONFIRM_URL": "username/reset/confirm/{uid}/{token}",
#     # "ACTIVATION_URL": "activate/{uid}/{token}",
#     "ACTIVATION_URL": "user/activate/{uid}/{token}",
#     # "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": ["http://manap.django-local.org:8002/"],
#     'EMAIL': {
#         'activation': 'AuthBillet.email.ActivationEmail',
#         'confirmation': 'AuthBillet.email.ConfirmationEmail',
#         'password_reset': 'AuthBillet.email.PasswordResetEmail',
#         'password_changed_confirmation': 'AuthBillet.email.PasswordChangedConfirmationEmail',
#         'username_changed_confirmation': 'AuthBillet.email.UsernameChangedConfirmationEmail',
#         'username_reset': 'AuthBillet.email.UsernameResetEmail',
#     },
# }

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "www", "static")
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "www", "media")
MEDIA_URL = '/media/'

# EMAIL
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', True)

# Celery Configuration Options
CELERY_TIMEZONE = os.environ.get('TIME_ZONE', 'UTC')
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND', 'redis://redis:6379/0')
# DJANGO_CELERY_BEAT_TZ_AWARE=False

# CHANNELS
ASGI_APPLICATION = "TiBillet.asgi.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}

# -------------------------------------/
# COMMUNECTER SSO oauth2
# -------------------------------------/
OAUTH_URL_WHITELISTS = []
OAUTH_CLIENT_NAME = 'communecter'
OAUTH_CLIENT = {
    'name':'communecter',
    'client_id': os.environ.get('COMMUNECTER_SSO_CLIENTID'),
    'client_secret': os.environ.get('COMMUNECTER_SSO_SECRET'),
    'access_token_url': 'https://sso.communecter.org/oauth/token',
    'authorize_url': 'https://sso.communecter.org/oauth/authorize',
    'api_base_url': 'https://sso.communecter.org/oauth',
    'redirect_uri': 'https://www.tibillet.org/api/user/oauth',
    'client_kwargs': {
        'scope': 'openid profile email',
        'token_placement': 'header'
    },
    'userinfo_endpoint': 'user',
}
OAUTH_COOKIE_SESSION_ID = 'sso_session_id'

# -------------------------------------/


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'tenant_context': {
            '()': 'django_tenants.log.TenantContextFilter'
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
            'datefmt': '%y %b %d, %H:%M:%S',
        },
        'tenant_context': {
            'format': '[%(schema_name)s:%(domain_url)s] '
                      '%(levelname)-7s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['tenant_context'],
        },
        'logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f"{BASE_DIR}/logs/Djangologfile",
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
            'filters': ['tenant_context'],
        },
        'weasyprint': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f"{BASE_DIR}/logs/weasyprint",
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
            'filters': ['tenant_context'],
        },
    },
    'root': {
        'level': 'INFO',
        # 'handlers': ['console', 'logfile', 'weasyprint']
        'handlers': ['console']
    },
}

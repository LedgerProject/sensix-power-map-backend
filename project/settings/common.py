"""
Common Settings.
"""
import datetime
import os
from itertools import chain

from apps.geo import choices
from project.settings.config import cfg

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

SECRET_KEY = cfg.get('SECRET_KEY', '3gSDCrozewyVAgZTcgtV1EzVvOS83C7gBEr7zdb/GiYOPWaV0i')

ALLOWED_HOSTS = cfg.get('ALLOWED_HOSTS', ['*'])

ENV_ID = cfg.get('ENV_ID', 'dev')
PROD_ENV_IDS = ['prod', 'staging']

DATABASES = cfg.get('DATABASES')

CACHES = cfg.get('CACHES', {})

CUSTOMERS = dict(cfg.get('CUSTOMERS', []))

SERVICES = cfg.get('SERVICES')

ADMIN_USERNAME = cfg.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = cfg.get('ADMIN_PASSWORD', 'mock@sensidev!pwd')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_EMAIL_ADDRESS = 'say@sensix.io'

DEVICE_METRICS_FILE_PATH = cfg.get('DEVICE_METRICS_FILE_PATH', os.path.join(BASE_DIR, 'device_metrics_conf.json'))

MOVING_AVERAGE_DEFAULT_KEY = 'r3'
MOVING_AVERAGE_OPTIONS = {
    'r3': {
        'range': 3 * 60 * 60,  # 3 hours
        'window': 600,  # 10 min
    },
    'r8': {
        'range': 8 * 60 * 60,  # 8 hours
        'window': 1600,  # ~27 min
    },
    'r24': {
        'range': 24 * 60 * 60,  # 24 hours
        'window': 4800,  # 80 min
    },
    'r48': {
        'range': 48 * 60 * 60,  # 48 hours
        'window': 9600,  # 160 min
    }
}

VALUE_PRECISION = 2

THD_AGG_VOLTAGE_METRIC_KEY = 'THV'
THD_AGG_CURRENT_METRIC_KEY = 'THI'

THD_VOLTAGE_METRIC_KEYS = ['THV1', 'THV2', 'THV3']  # Voltage Total Harmonic Distortions
THD_CURRENT_METRIC_KEYS = ['THI1', 'THI2', 'THI3']  # Current Total Harmonic Distortions

THD_METRIC_KEYS = THD_VOLTAGE_METRIC_KEYS + THD_CURRENT_METRIC_KEYS

CATEGORY_METRIC_KEYS_MAP = {
    choices.CATEGORY_POWER_QUALITY_ID: THD_METRIC_KEYS + [
        # L1 Odd Voltage harmonic distortions
        '1V3', '1V5', '1V7', '1V9', '1V11', '1V13', '1V15', '1V17', '1V19', '1V21', '1V23', '1V25', '1V27', '1V29',
        '1V31', '1V33', '1V35', '1V37', '1V39',
        # L2 Odd Voltage harmonic distortions
        '2V3', '2V5', '2V7', '2V9', '2V11', '2V13', '2V15', '2V17', '2V19', '2V21', '2V23', '2V25', '2V27', '2V29',
        '2V31', '2V33', '2V35', '2V37', '2V39',
        # L3 Odd Voltage harmonic distortions
        '3V3', '3V5', '3V7', '3V9', '3V11', '3V13', '3V15', '3V17', '3V19', '3V21', '3V23', '3V25', '3V27', '3V29',
        '3V31', '3V33', '3V35', '3V37', '3V39',
        # L1 Odd Current harmonic distortions
        '1I3', '1I5', '1I7', '1I9', '1I11', '1I13', '1I15', '1I17', '1I19', '1I21', '1I23', '1I25', '1I27', '1I29',
        '1I31', '1I33', '1I35', '1I37', '1I39',
        # L2 Odd Current harmonic distortions
        '2I3', '2I5', '2I7', '2I9', '2I11', '2I13', '2I15', '2I17', '2I19', '2I21', '2I23', '2I25', '2I27', '2I29',
        '2I31', '2I33', '2I35', '2I37', '2I39',
        # L3 Odd Current harmonic distortions
        '3I3', '3I5', '3I7', '3I9', '3I11', '3I13', '3I15', '3I17', '3I19', '3I21', '3I23', '3I25', '3I27', '3I29',
        '3I31', '3I33', '3I35', '3I37', '3I39',
    ],
    choices.CATEGORY_POWER_USAGE_ID: [
        'Pc',  # Cumulated Total Active Power
        'SPc',  # Cumulated Apparent Power
        'fSPc'  # Cumulated Reactive Power
    ]
}

ELIGIBLE_METRIC_KEYS = list(chain.from_iterable([metric_keys for metric_keys in CATEGORY_METRIC_KEYS_MAP.values()]))
ELIGIBLE_DEVICE_TYPES = cfg.get('ELIGIBLE_DEVICE_TYPES', ['1P-PowerMonitor1', '3PN-PowerMonitor1'])

CORS_ORIGIN_WHITELIST = cfg.get('CORS_ORIGIN_WHITELIST', ())

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_framework_swagger',
]

HELPER_APPS = [
    'corsheaders',
    'django_select2',
    'cacheback',
    'django_json_widget',
    'django_rq',
    'defender',
]

APPS = [
    'apps.core',
    'apps.geo',
]

INSTALLED_APPS = DJANGO_APPS + HELPER_APPS + APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'defender.middleware.FailedLoginMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_TZ = False

FIRST_DAY_OF_WEEK = 1

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = cfg.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static'))
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_ROOT = cfg.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))
MEDIA_URL = '/media/'

SESSION_COOKIE_NAME = 'eq-users-session-id'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=180),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': cfg.get('JWT_SECRET_KEY', SECRET_KEY),

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'username',
    'USER_ID_CLAIM': 'usr',
    'TOKEN_TYPE_CLAIM': 'typ',
    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(hours=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=180),
}

REST_SESSION_LOGIN = False
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'PAGE_SIZE': 1000,
    'DEFAULT_SCHEMA_CLASS': 'common.schemas.CustomSchema',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '120/hour',
    },
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
    'EXCEPTION_HANDLER': 'apps.core.exceptions.message_exception_handler',
}

SELECT2_CACHE_BACKEND = 'default'

CACHEBACK_TASK_QUEUE = 'rq'
DEFAULT_CACHE_DURATION_SECONDS = 60
LIVE_METRICS_CACHE_TIMEOUT_SECONDS = 60

MIGRATION_MODULES = {
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'LOGIN_URL': '/admin/login/',
    'LOGOUT_URL': '/admin/logout/',
    'JSON_EDITOR': False,
    'VALIDATOR_URL': None,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(funcName)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'rq_console': {
            'format': '%(asctime)s %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
        },
        'rq_console': {
            'level': 'DEBUG',
            'class': 'rq.utils.ColorizingStreamHandler',
            'formatter': 'rq_console',
            'exclude': ['%(asctime)s'],
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        }
    },
}

try:
    from .integrations.sentry import *
    from .integrations.defender import *
    from .integrations.mqtt import *
    from .integrations.rq import *
except ImportError as e:
    if cfg.get('SENTRY_IO_ENABLED', False):
        import sentry_sdk

        sentry_sdk.capture_exception(e)
        raise e

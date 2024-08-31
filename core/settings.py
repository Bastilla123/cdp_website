from django.contrib.messages import constants
import ast
import os
from dotenv import load_dotenv
from unipath import Path
from django.utils.translation import gettext_lazy as _
from decouple import config

load_dotenv()



location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMAIL_BACKEND = 'backend.email.EmailBackend'
EMAIL_HOST = 'mail.beelze-solutions.de'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'postmaster@beelze-solutions.de'
EMAIL_HOST_PASSWORD = 'fsjZV2XKmXFBTw2RyacD'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

SECRET_KEY = 'eyJmb28iOiJiYXIifQ:1kx6Rf:LBB39RQmME-SRvilheUe5EmPYRbuDBgQp2tCAi7KGLk'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG   = True
DEVEL   = os.getenv('DEVEL', False)
SERVER  = os.getenv('DEVEL', '127.0.0.1')

# load production server from .env
ALLOWED_HOSTS = ['*']

APPEND_SLASH=False

CDC_SERVER = config('CDC_SERVER')

CDC_APIKEY = config('CDC_APIKEY')
CDC_SECRET = config('CDC_SECRET')
CDC_USERKEY = config('CDC_USERKEY')
CDC_LOCALLIST = config('CDC_LOCALLIST')

SEND_EMAIL = config('SEND_EMAIL', cast=bool)

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MESSAGE_TAGS = {
    constants.DEBUG: 'info',
    constants.INFO: 'info',
    constants.SUCCESS: 'success',
    constants.WARNING: 'warning',
    constants.ERROR: 'danger',
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',  # Enable the inner app
    'customers',
    'rest_framework',
'django_middleware_global_request',
    'order', #Bestellstrecke
'crispy_forms',
    "crispy_bootstrap5"
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
    'django.middleware.locale.LocaleMiddleware',
'django_middleware_global_request.middleware.GlobalRequestMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"   # Route defined in app/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in app/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "core/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.middleware.middleware'
            ],
        },
    },
]

LOGIN_URL = '/login/'

DATABASES = {
        'default': {
            'ENGINE': config('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
            'NAME': config('DATABASE_NAME', None),
            'USER': config('DATABASE_USER', None),
            'PASSWORD': config('DATABASE_PASSWORD', None),
            'HOST': config('DATABASE_HOST', None),
            'PORT': config('DATABASE_PORT', None),
            'ATOMIC_REQUESTS': True
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(CORE_DIR, 'media')

MEDIA_URL = '/media/'

BASE_DIR = Path(__file__).parent.parent



STATICFILES_DIRS = [
os.path.join(BASE_DIR, "core/static")
]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',


)

CDP_BUSINESSUNIT = "4_p4oH0IcAbAPkEilVFaaiWQ"
CDP_EVENT_LIST = {"change_profile":{"cdp_applicationid" :"HDJZr4y39x1wqgLMneGSIQ","cdp_eventid":"HEHA7LsdP2Owa5whR2rjaw"},
                   "new_contact":{"cdp_applicationid" :"HDJZr4y39x1wqgLMneGSIQ","cdp_eventid":"HNAC7ti_Z4d6H6dwgz1z4A"},} #List of different applications/events of cdp


CDP_API_USERNAME = config('CDP_API_USERNAME')
CDP_API_PASSWORD = config('CDP_API_PASSWORD')
CDP_API_BASEURL = config('CDP_API_BASEURL')
CDP_BUSINESSUNIT = config('CDP_BUSINESSUNIT', None)
CDP_EVENT_LIST = config('CDP_EVENT_LIST', None)
CDP_EVENT_LIST = ast.literal_eval(CDP_EVENT_LIST)

BASE_TEMPLATE = config('BASE_TEMPLATE')
APP_TITLE = config('APP_TITLE', None)

LANGUAGE_CODE = 'de-de'
USE_I18N = True
USE_L10N = False
DATE_INPUT_FORMATS = ('%d.%m.%Y','%d-%m-%Y','%Y-%m-%d')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


LANGUAGES = [
('de', _('German')),
('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(CORE_DIR,  'locale/'),
]

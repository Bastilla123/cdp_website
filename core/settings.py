

import os, random, string
from dotenv import load_dotenv
from unipath import Path
import dj_database_url
from django.utils.translation import gettext_lazy as _
from decouple import config

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG   = os.getenv('DEBUG', True)
DEVEL   = os.getenv('DEVEL', False)
SERVER  = os.getenv('DEVEL', '127.0.0.1')

# load production server from .env
ALLOWED_HOSTS = ['*']

APPEND_SLASH=False

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
#SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
#SESSION_COOKIE_NAME = 'database_sa'
#SESSION_COOKIE_DOMAIN = '127.0.0.1'
#WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(CORE_DIR, 'media')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'core/static'),
)

#SESSION_COOKIE_AGE = 1209600
#SESSION_SAVE_EVERY_REQUEST = False

#CDP

# CDP_API_USERNAME = 'AE+WNj6Fu6YE'
# CDP_API_PASSWORD = '77iAGD7vXyEMPIi9HB0sR1GNGKOcHZbh'
# CDP_API_BASEURL = 'https://cdp.EU5-prod.gigya.com'
# CDP_BUSINESSUNIT = "4_p4oH0IcAbAPkEilVFaaiWQ"
# CDP_EVENT_LIST = {"change_profile":{"cdp_applicationid" :"HDJZr4y39x1wqgLMneGSIQ","cdp_eventid":"HEHA7LsdP2Owa5whR2rjaw"},
#                   "new_contact":{"cdp_applicationid" :"HDJZr4y39x1wqgLMneGSIQ","cdp_eventid":"HNAC7ti_Z4d6H6dwgz1z4A"},} #List of different applications/events of cdp


CDP_API_USERNAME = config('CDP_API_USERNAME', None)
CDP_API_PASSWORD = config('CDP_API_PASSWORD', None)
CDP_API_BASEURL = config('CDP_API_BASEURL', None)
CDP_BUSINESSUNIT = config('CDP_BUSINESSUNIT', None)
CDP_EVENT_LIST = config('CDP_EVENT_LIST', None)

APP_TITLE = config('APP_TITLE', None)

LANGUAGE_CODE = 'de-de'
USE_I18N = True
USE_L10N = False
DATE_INPUT_FORMATS = ('%m/%d/%Y','%d-%m-%Y','%Y-%m-%d')


LANGUAGES = [
('de', _('German')),
('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(CORE_DIR,  'locale/'),
]

#############################################################
#############################################################

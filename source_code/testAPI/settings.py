"""
Django settings for web_service project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
# import sys
import datetime
# from socket import gethostname, gethostbyname, gethostbyname_ex

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# PYINSTRUMENT_PROFILE_DIR = 'profiles'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^1ae+k*1111(c+0sidyz#!$111^6=qk(t8+m8wsmh@k-11161a'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False


# ALLOWED_HOSTS = [gethostname(), gethostbyname(gethostname()), '127.0.0.1', 'localhost', '174.129.126.138']
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', gethostname()] + gethostbyname_ex(gethostname())[2]
ALLOWED_HOSTS = ['*', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'test',
    'rest_framework',
    'background_task'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'test.middleware.LoggingMiddleware',
]

# if DEBUG:
#     MIDDLEWARE.extend([
#         #  'django.middleware.security.SecurityMiddleware',
#         #  'django.contrib.sessions.middleware.SessionMiddleware',
#         #  'django.middleware.common.CommonMiddleware',
#         #  'django.middleware.csrf.CsrfViewMiddleware',
#         #  'django.contrib.auth.middleware.AuthenticationMiddleware',
#         #  'django.contrib.messages.middleware.MessageMiddleware',
#         #  'django.middleware.clickjacking.XFrameOptionsMiddleware',
#         'pyinstrument.middleware.ProfilerMiddleware'
#     ])

ROOT_URLCONF = 'testAPI.urls'

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

WSGI_APPLICATION = 'testAPI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_sql.sqlite3'),
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'test',
    #     'HOST': '127.0.0.1',
    #     'USER': 'root',
    #     'PASSWORD': '',
    # }
}
# AUTHENTICATION_BACKENDS = (
#     'mongoengine.django.auth.MongoEngineBackend',
# )
# MONGO_DATABASE_NAME = 'snatchbot'
# from mongoengine import connect
# connect('snatchbot', host='mongodb://localhost',  port=27017)
# connect(MONGO_DATABASE_NAME)
# import mongoengine
# mongoengine.connect('snatchbot', host='mongodb://localhost',  port=27017)

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        # custom parser to JSON
        'lib.json_encoder.JSONRender',
        # default API
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# background_task config

BACKGROUND_TASK_RUN_ASYNC = True

# MAX_RUN_TIME = 3600*24*14
MAX_RUN_TIME = 60

MAX_ATTEMPTS = 10

# Media files

_PATH = os.path.abspath(os.path.dirname(__file__))

if not os.path.isdir(os.path.join(_PATH, 'files')):
    os.makedirs(os.path.join(os.path.join(_PATH, 'files')))

MEDIA_ROOT = os.path.join(_PATH, 'files')
MEDIA_URL = '/file/'


LOG_FILE_NAME = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
if not os.path.isdir(os.path.join(_PATH, 'loggins')):
    os.makedirs(os.path.join(_PATH, 'loggins'))

LOGGING = {
    'version': 1,
    'disable_existing_liggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(_PATH, 'loggins', LOG_FILE_NAME),
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 100,
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.request': {
            'level': 'DEBUG',
            'handlers': ['file']
        },
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        '': {
            'level': 'DEBUG',
           'handlers': ['file']
        }
    }
}
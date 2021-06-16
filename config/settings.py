import os
from pathlib import Path

import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# Load operating system environment variables and then prepare to use them
env = environ.Env()
env_file = str(BASE_DIR / '.env')
env.read_env(env_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-f^n19ezo)%ja=acz*$@)*$h4x*!4%0vr$-z_h4!pg)=vv1v9n*')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # rest-framework apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # social accounts
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.gitlab',
    'allauth.socialaccount.providers.bitbucket_oauth2',

    # encrypted model fields
    'encrypted_model_fields',

    # swag_auth
    'swag_auth',

    # my apps
    'universal_doc_importer.apps.UniversalDocImporterConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SWAGAUTH_SETTINGS = {
    'bitbucket': {
        'APP': {
            'key': env.str('BITBUCKET_KEY'),
            'secret': env.str('BITBUCKET_SECRET'),
        },
        'SCOPE': [
            'repository',
        ],
    },
    'github': {
        'APP': {
            'client_id': env.str('GITHUB_CLIENT_ID'),
            'secret': env.str('GITHUB_SECRET'),
            'key': '',
        },
        'SCOPE': [
            'repo',
        ],
        'CALLBACK_ULR': 'http://127.0.0.1:8000/swag/github/callback/',
    },
    'gitlab': {
        'APP': {
            'client_id': env.str('GITLAB_CLIENT_ID'),
            'secret': env.str('GITLAB_SECRET'),
            'key': '',
        },
        'SCOPE': [
            'read_repository',
            'api',
        ]
    }
    # TODO: other services
}

# Django encrypted model fields
# https://pypi.org/project/django-encrypted-model-fields/
# run ./manage.py generate_encryption_key and set the value in the environment
# TODO: Add default value
FIELD_ENCRYPTION_KEY = env('FIELD_ENCRYPTION_KEY')

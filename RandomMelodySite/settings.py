"""
Django settings for RandomMelodySite project.

Generated by 'django-admin startproject' using Django 3.2.8.

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

# SECRET_KEY = os.environ.get('RM_SITE_SECRET_KEY')

#SECRET_KEY = str(os.environ['RM_SITE_SECRET_KEY'])
SECRET_KEY = os.getenv("RM_SITE_SECRET_KEY") 

# SECURITY WARNING: don't run with debug turned on in production!
# True - UnDeployed
# False - Deployed
DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1","https://random-melody-site.herokuapp.com/"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'mainapp',

    'storages',

    #'django_extensions', # for validating templates, tests, etc
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "whitenoise.middleware.WhiteNoiseMiddleware"
]

ROOT_URLCONF = 'RandomMelodySite.urls'

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

WSGI_APPLICATION = 'RandomMelodySite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

TIME_ZONE = 'Israel'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = '/'

MAINAPP_NAME = 'mainapp'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/



# STATIC_URL' is for Django to {% load static %} and more static refs in html templates. 
STATIC_URL = '/static/'


# 'STATIC_ROOT' : single root directory from where the Django application will copy all static files in your project to 'staticfiles' folder and serve the static files *AFTER DEPLOYMENT* in production:

STATIC_ROOT = os.path.join(BASE_DIR, "static") # Default  

if DEBUG == True: # if the site isn't Deployed yet:
    STATIC_ROOT  = os.path.join(BASE_DIR, MAINAPP_NAME, "static")

if DEBUG == False: # if the site is Deployed:
    STATIC_ROOT  = os.path.join(BASE_DIR, 'staticfiles')


MIDIFILES_PATH = os.path.join(STATIC_ROOT, MAINAPP_NAME, 'MidiFiles')



# S3 Bucket CONFIG:

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import django_heroku
# Activate Django-Heroku.
django_heroku.settings(locals())

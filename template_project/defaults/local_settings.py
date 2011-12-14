# -*- coding: utf-8 -*-
import os, sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_NAME = 'template_project'
PROJECT_TITLE = u'Шаблонный проект'
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

ROOT_URLCONF = '%s.urls' % PROJECT_NAME

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s/db/%s.sqlite' % (PROJECT_DIR, PROJECT_NAME),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '%s/cache' % PROJECT_DIR,
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
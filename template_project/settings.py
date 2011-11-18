# -*- coding: utf-8 -*-
import os, sys

from local_settings import *

MY_DJANGO_ROOT = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-2])
sys.path.append(MY_DJANGO_ROOT)
sys.path.append(MY_DJANGO_ROOT+'/apps')
sys.path.append(PROJECT_DIR)

from common.settings import *

SITE_ID=1

MEDIA_URL = '/media/'
MEDIA_ROOT = PROJECT_DIR + '/media/'

STATIC_URL = MEDIA_URL
STATIC_ROOT = MEDIA_ROOT

ADMIN_MEDIA_PREFIX = '/admin_media/'
ADMIN_MEDIA_ROOT = MY_DJANGO_ROOT + '/admin_media/'

SECRET_KEY = '8!&d=_!md4nzvv0i658(vnyzdfdf_)-@b39g$_0+-oer3s0872'

ROOT_URLCONF = '%s.urls' % PROJECT_NAME

TEMPLATE_DIRS = (
    PROJECT_DIR + "/website/templates",
    MY_DJANGO_ROOT + "/apps/common/templates",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.sites',
    'common',
    'filebrowser',
    'tinymce',
    'mptt',
    'treeadmin',
    'south',
    'seo',
    'pages',
    'website',
)

# MESSAGES
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# FILEBROWSER
FILEBROWSER_URL_FILEBROWSER_MEDIA = os.path.join(ADMIN_MEDIA_PREFIX , 'filebrowser/')
FILEBROWSER_PATH_FILEBROWSER_MEDIA = os.path.join(ADMIN_MEDIA_ROOT , 'filebrowser/')
FILEBROWSER_URL_TINYMCE = os.path.join(ADMIN_MEDIA_PREFIX , 'tiny_mce/')
FILEBROWSER_PATH_TINYMCE = os.path.join(ADMIN_MEDIA_ROOT , 'tiny_mce/')

FILEBROWSER_VERSIONS_BASEDIR = '_versions_'
FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 40, 'height': 40, 'opts': 'upscale'},
}
FILEBROWSER_ADMIN_VERSIONS = ['fb_thumb']
FILEBROWSER_ADMIN_THUMBNAIL ='fb_thumb'

# CAPTCHA SETTINGS
CAPTCHA_CACHE_PREFIX = PROJECT_NAME+"_captcha_"

# TINYMCE SETTINGS
TINYMCE_JS_ROOT = os.path.join(ADMIN_MEDIA_ROOT, 'tiny_mce')
TINYMCE_JS_URL = os.path.join(ADMIN_MEDIA_PREFIX, 'tiny_mce/tiny_mce.js')

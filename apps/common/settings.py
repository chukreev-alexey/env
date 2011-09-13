# -*- coding: utf-8 -*-
import os

ADMINS = (
    ('Errors', 'errors@itcase.ru'),
    #('Alexey', 'chukreev.alexey@itcase.ru'),
    #('Arkadiy', 'arkadiy@itcase.ru'),
    #('Anton', 'anton_b@itcase.ru'),
)
MANAGERS = ADMINS

TIME_ZONE = 'Asia/Yekaterinburg'
LANGUAGE_CODE = 'ru-RU'

USE_I18N = True
USE_L10N = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pages.middleware.PageMiddleware',
)

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


FILE_UPLOAD_PERMISSIONS = 0644

FILEBROWSER_DEFAULT_SORTING_BY = 'filetype_checked'
FILEBROWSER_DEFAULT_SORTING_ORDER = 'asc'

#Regional settings
MONTHS = {1: u'января', 2: u'февраля', 3: u'марта',
          4: u'апреля', 5: u'мая', 6: u'июня',
          7: u'июля', 8: u'августа', 9: u'сентября',
          10: u'октября', 11: u'ноября', 12: u'декабря'}
ONE_MONTHS = {1: u'январь', 2: u'февраль', 3: u'март',
              4: u'апрель', 5: u'май', 6: u'июнь',
              7: u'июль', 8: u'август', 9: u'сентябрь',
              10: u'октябрь', 11: u'ноябрь', 12: u'декабрь'}

TINYMCE_DEFAULT_CONFIG = {   
    'plugins' : "safari,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",
    'theme': "advanced",
    'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,|,styleselect,formatselect",
    'theme_advanced_buttons2' : "cut,copy,paste,pasteword,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,code,|,forecolor,backcolor",
    'theme_advanced_buttons3' : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,iespell,media,advhr,|,fullscreen",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    'theme_advanced_statusbar_location' : "bottom",
    'theme_advanced_resizing' : "true",
}
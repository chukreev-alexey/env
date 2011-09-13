# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('seo.views',
    url(r'^robots\.txt$', 'robots', name='robots.txt')
)
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from common.urls import urlpatterns as common_urls

urlpatterns = common_urls





# Serving static
if settings.DEBUG:
    urlpatterns += patterns('django.views',
        url(r'^media/(?P<path>.*)$', 'static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

# Includes
urlpatterns += patterns('',
    (r'', include('seo.urls')),
)

urlpatterns += patterns('website.views',
    url(r'^messages/$', 'message_list', name='message_list'),
    url(r'^messages/(.*)/$', 'message_list', name='message_list'),
    url(r'^(?P<page_url>.*?)[/]?$', 'page', name="page"),
)
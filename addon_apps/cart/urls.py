# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('cart.views',
    (r'add/$', 'add_cart'),
    (r'update/$', 'update_cart'),
    url(r'delete/(?P<id>\d+)/$', 'delete_cart', name='delete_cart'),
    (r'empty/$', 'empty_cart'),
    url(r'order/$', 'order_cart', name='order_cart'),
    url(r'$', 'show_cart', name='show_cart'),
)
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from settings import MONTHS

def get_paginator(request, queryset, rows_on_page=None, pages_forward=None):
    DEFAULT_ROWS_ON_PAGE = 30
    DEFAULT_PAGES_FORWARD = 5
    rows_on_page = rows_on_page or DEFAULT_ROWS_ON_PAGE
    pages_forward = pages_forward or DEFAULT_PAGES_FORWARD 
    
    paginator = Paginator(queryset, rows_on_page, orphans=0)
    try:
        page = int(request.REQUEST.get('page', '1'))
    except ValueError:
        page = 1
    try:
        objects = paginator.page(page)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)
    
    start_index = page - (pages_forward+1)
    if start_index < 0:
       start_index = 0
    objects.paginator.slice = "%d:%d" % (start_index, page+pages_forward)
    return objects

def get_int_key(arr, key):
    if arr.get(key, False):
        try:
            return int(arr[key])
        except:
            pass
    return False    
    
def intlist(arr):
    for item in arr:
        try:
            yield int(item)
        except:
            pass

def rus_date(value):
    return u"%d %s" % (value.day, MONTHS[value.month])

def rus_full_date(value):
    return u"%d %s %d" % (value.day, MONTHS[value.month], value.day)
    
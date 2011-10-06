# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import generic

from models import Gallery

class GalleryInline(generic.GenericTabularInline):
    model = Gallery
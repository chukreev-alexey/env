# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from filebrowser.fields import FileBrowseField
        
class Gallery(models.Model):
    name = models.CharField(u'Название', max_length=255, blank=True, null=True)
    image = FileBrowseField(u'Картинка', format='Image', max_length=255)
    sort = models.IntegerField(u'Порядок', default=0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    def __unicode__(self):
        return ''
    class Meta:
        ordering = ('sort', )
        verbose_name = u'фото'
        verbose_name_plural = u'фото галерея'

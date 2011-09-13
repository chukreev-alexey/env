# -*- coding: utf-8 -*-

from django.db import models

class VisibleObjectManager(models.Manager):
    def get_query_set(self):
        return super(VisibleObjectManager, self).get_query_set().filter(visible=True)

class VisibleObject(models.Model):
    visible = visible = models.BooleanField(u'Показывать?', default=False)
    allpages = models.Manager()
    objects = VisibleObjectManager()
    class Meta:
        abstract = True

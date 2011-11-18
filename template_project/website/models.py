# -*- coding: utf-8 -*-
from django.db import models
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.urlresolvers import reverse

from common.fields import MultiEmailField
from filebrowser.fields import FileBrowseField
from tinymce import models as tinymce_models

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^common\.fields\.MultiEmailField"])

class VisibleObjects(models.Manager):
    def get_query_set(self):
        return super(VisibleObjects, self).get_query_set().filter(visible=True)

class Settings(models.Model):
    project = models.CharField(u'Название проекта', max_length=255)
    email = MultiEmailField(u'Email для писем', max_length=255,
        help_text=u'''Можете вставить несколько email, разделив их запятой''')
    
    def __unicode__(self):
        return u'настройки'
            
    class Meta:
        verbose_name = u'настройки'
        verbose_name_plural = u'настройки'

@receiver(post_save, sender=Settings)
@receiver(post_delete, sender=Settings)
def clear_settings_cache(sender, **kwargs):
    cache.delete('settings')
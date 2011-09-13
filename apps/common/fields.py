# -*- coding: utf-8 -*-
import re
from django.db import models
from django.core.validators import validate_email
from south.modelsinspector import add_introspection_rules

def emails_list(value):
    return filter(lambda x: bool(x.strip()), re.split(r'[,|;]?\s?', value or ''))

class MultiEmailField(models.CharField):
    def validate(self, value, model_instance):
        super(MultiEmailField, self).validate(value, model_instance)
        for email in emails_list(value):
            validate_email(email)


add_introspection_rules([], ["^common\.fields\.MultiEmailField"])

class ManyToManyFieldNoTable(models.ManyToManyField):
    def __init__(self, *args, **kwargs):
        super(ManyToManyFieldNoTable, self).__init__(*args, **kwargs)
        self.creates_table = False
rules = [
    (
        (models.ManyToManyField,),
        [],
        {
            "to": ["rel.to", {}],
            "symmetrical": ["rel.symmetrical", {"default": True}],
            "related_name": ["rel.related_name", {"default": None}],
            "db_table": ["db_table", {"default": None}],
            # TODO: Kind of ugly to add this one-time-only option
            "through": ["rel.through", {"ignore_if_auto_through": True}],
        }
    )
]
add_introspection_rules(rules, ["^common\.fields\.ManyToManyFieldNoTable"])


        
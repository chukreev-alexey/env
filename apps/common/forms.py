# -*- coding: utf-8 -*-
from django import forms

def as_eul(self):
    return self._html_output(
        normal_row = u'<li%(html_class_attr)s><div class="FormLabel">%(label)s</div> <div class="FormField">%(field)s</div><div class="FormError">%(errors)s</div><div class="FormHelpText">%(help_text)s</div></li>',
        error_row = u'<li>%s</li>',
        row_ender = '</li>',
        help_text_html = u' %s',
        errors_on_separate_row = False)
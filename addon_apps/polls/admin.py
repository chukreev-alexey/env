# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from models import Poll, Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'answer':
            kwargs['widget'] = forms.Textarea(attrs={'rows':'5'})
        return super(AnswerInline, self).formfield_for_dbfield(db_field, **kwargs)

class PollAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview', 'all_votes', 'dt_mod', 'active')
    list_editable = ('active', )
admin.site.register(Poll, PollAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'poll', 'admin_get_answers', 'multi_choice',
                    'sort')
    list_filter = ('poll', )
    list_editable = ('multi_choice', 'sort')
    inlines = [AnswerInline]
admin.site.register(Question, QuestionAdmin)
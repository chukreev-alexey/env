# -*- coding: utf-8 -*-
import datetime

from django import forms
from django.db import models

def as_eul(self):
    return self._html_output(
        normal_row = u'<li%(html_class_attr)s><div class="FormLabel">%(label)s</div> <div class="FormField">%(field)s</div><div class="FormError">%(errors)s</div><div class="FormHelpText">%(help_text)s</div></li>',
        error_row = u'<li>%s</li>',
        row_ender = '</li>',
        help_text_html = u' %s',
        errors_on_separate_row = False)
forms.BaseForm.as_eul = as_eul

class Poll(models.Model):
    name = models.CharField(u'Заголовок', max_length=255)
    preview = models.TextField(u'Описание', blank=True, null=True)
    active = models.BooleanField(u'Активен', default=False)
    all_votes = models.IntegerField(u'Проголосовало', default=0)
    dt_mod = models.DateTimeField(u'Дата создания',
                                  default=datetime.datetime.now)
    
    def get_form(self, data=None):
        form = forms.Form(data)
        form.fields['poll'] = \
            forms.CharField(widget=forms.HiddenInput, initial=self.pk)
        for question in self.questions.all():
            if question.multi_choice:
                form.fields['question_%d' % question.pk] = \
                    forms.ModelMultipleChoiceField(label=question.question,
                        queryset=question.answers,
                        error_messages={'required': u'Пожалуйста, выберите вариант ответа'},
                        widget=forms.CheckboxSelectMultiple)
            else:
                form.fields['question_%d' % question.pk] = \
                    forms.ModelChoiceField(label=question.question,
                        queryset=question.answers, empty_label=None,
                        error_messages={'required': u'Пожалуйста, выберите вариант ответа'},
                        widget=forms.RadioSelect)
        return form
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('-dt_mod', )
        verbose_name = u'опрос'
        verbose_name_plural = u'опросы'

class Question(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=u'Опрос',
                             related_name='questions')
    question = models.TextField(u'Вопрос')
    sort = models.IntegerField(u'Порядок', default=0)
    multi_choice = models.BooleanField(u'Мульти выбор?', default=False)
    
    def admin_get_answers(self):
        return u'<ul>%s</ul>' % \
            ''.join([u'<li>%s %.2f%%</li>' % (item.answer,
                (100.0 * item.votes) / (1 if self.poll.all_votes == 0 else self.poll.all_votes))
                for item in self.answers.all()])
    admin_get_answers.short_description = u'Ответы'
    admin_get_answers.allow_tags = True
    
    def __unicode__(self):
        return self.question
    
    class Meta:
        ordering = ('sort', )
        verbose_name = u'вопрос'
        verbose_name_plural = u'вопросы'

class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name=u'Вопрос',
                                 related_name='answers')
    answer = models.TextField(u'Ответ')
    votes = models.IntegerField(u'Кол-во ответивших', default=0)
    sort = models.IntegerField(u'Порядок', default=0)
    
    def get_percent(self):
        all = self.question.poll.all_votes
        return 100.0 * self.votes / (1 if all == 0 else all)
    
    def __unicode__(self):
        return self.answer
    
    class Meta:
        ordering = ('sort', )
        verbose_name = u'ответ'
        verbose_name_plural = u'ответы'
    
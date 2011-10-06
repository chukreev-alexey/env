# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import transaction

from polls.models import Poll, Answer  

def _get_poll(pk=None):
    if pk:
        try:
            return Poll.objects.get(pk=pk)
        except Poll.DoesNotExist:
            return None
    try:
        return Poll.objects.filter(active=True)[0]
    except IndexError:
        return None

@transaction.commit_on_success        
def _process_poll_form(request, pk=None):
    if request.method == 'POST': # Post answers
        poll = get_object_or_404(Poll, pk=request.POST.get('poll', 0))
        form = poll.get_form(request.POST)
        if form.is_valid():
            for key, answers in form.cleaned_data.items():
                if isinstance(answers, Answer):
                    answers = [answers]
                for item in answers:
                    if isinstance(item, Answer):
                        item.votes += 1
                        item.save()
            poll.all_votes += 1
            poll.save()
            cookie_key = 'answered_poll_%d' % poll.pk
            response = HttpResponseRedirect('')
            response.set_cookie(cookie_key, value=str(poll.pk),
                                max_age=60*60*24*365, path='/')
            return response
    else:
        poll = _get_poll(pk)
        if not poll:
            return None, None
        cookie_key = 'answered_poll_%d' % poll.pk
        if request.COOKIES.get(cookie_key, False):
            return poll, None
        form = poll.get_form()
    return poll, form    

def poll_processing(func): # Very cool decorator
    def wrapper(*args, **kwargs):
        data = _process_poll_form(args[0])
        if isinstance(data, HttpResponseRedirect):
            return data # Return redirect response
        if isinstance(data, tuple) and len(data) == 2:
            args[0].poll_data = data[0]
            args[0].poll_form = data[1]
        return func(*args, **kwargs)
    return wrapper


        
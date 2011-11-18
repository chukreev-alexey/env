# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from common.fields import emails_list

def page(request, page_url):
    template = 'base.html'
    context = {}
    return render(request, template, context)

def message_list(request, arg=None):
    return render(request, 'messages.html')
        
def feedback(request):
    from website.forms import FeedbackForm
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = u'Вопрос с сайта'
            recipients = []
            recipients.extend(emails_list(request.settings.email))
            letter_context = form.cleaned_data
            letter_context.update({'site': request.settings.project})
            letter_content = render_to_string('feedback_letter.txt', letter_context)
            send_mail(subject, letter_content,
                      letter_context['email'] or recipients[0], recipients)
            messages.add_message(request, messages.SUCCESS, u"Ваше письмо успешно отправлено администрации сайта.")
            return redirect('')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})
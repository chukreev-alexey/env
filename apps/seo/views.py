# -*- coding: utf-8 -*-
import os

from django.http import Http404, HttpResponse
from django.conf import settings

def robots(request):
    path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'seo', 'robots.txt')
    if os.path.exists(path):
        return HttpResponse(open(path).read(), mimetype='text/plain')
    else:
        raise Http404
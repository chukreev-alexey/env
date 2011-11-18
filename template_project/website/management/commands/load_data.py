# -*- coding: utf-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import translation
from django.http import HttpRequest
from django.contrib import messages


class CommandExecutionError(object):
    """Класс для отображения ошибок в исполняемых командах.
    Если первым неименованным аргументом в команду передается объект
    HttpRequest, это значит, что команда запущена через интерфейс
    администратора, и ошибки будут накапливаться в стандартном хранилище для 
    сообщений http://docs.djangoproject.com/en/dev/ref/contrib/messages/.
    В противном случае будем считать, что запуск команды производился из
    командной строки. И ошибки будут выводиться в стандартный поток ошибок
    stderr, а сообщения будут просто печататься на экран.
    """
    def __init__(self, request):
        self.request = request if isinstance(request, HttpRequest) else None
        self.is_success = True
    
    def info(self, message):
        if self.request:
            messages.add_message(self.request, messages.SUCCESS,  message)
        else:
            print message.encode('utf-8')
    
    def warning(self, message):
        if self.request:
            messages.add_message(self.request, messages.WARNING,  message)
        else:
            print (u'Предупреждение: %s' % message).encode('utf-8')        
    
    def error(self, message):
        self.is_success = False
        if self.request:
            messages.add_message(self.request, messages.ERROR,  message)
        else:
            raise CommandError(message.encode('utf-8'))

class Command(BaseCommand):   
    help = u"Load data"
    requires_model_validation = False
    output_transaction = True
    option_list = BaseCommand.option_list + (
        make_option('--path', action='store', dest='path', help='Path to price file'),
    )
    def handle(self, *args, **options):
        path = options.get('path', None)
        
        translation.activate(settings.LANGUAGE_CODE)
        try:
            request = args[0]
        except IndexError:
            request = None
        log = CommandExecutionError(request)
        if not path:
            log.error(u'Не указан путь к загружаемому файлу')
            return
        #Код команды
        
        #Конец кода команды
        if log.is_success:
            log.info(u'Загрузка прошла успешно.')
        
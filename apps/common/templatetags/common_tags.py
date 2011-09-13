# -*- coding: utf-8 -*-
import re, math

from collections import defaultdict
from django import template
from django.utils.encoding import force_unicode
from django.core.cache import cache
from django.conf import settings

register = template.Library()

class CleverCacheNode(template.Node):
    def __init__(self, nodelist, expire_time_var, fragment_name):
        self.nodelist = nodelist
        self.expire_time_var = template.Variable(expire_time_var)
        self.fragment_name = fragment_name
    def render(self, context):
        try:
            expire_time = self.expire_time_var.resolve(context)
        except template.VariableDoesNotExist:
            raise template.TemplateSyntaxError('"clevercache" tag got an unknown variable: %r' % self.expire_time_var.var)
        try:
            expire_time = int(expire_time)
        except (ValueError, TypeError):
            raise template.TemplateSyntaxError('"clevercache" tag got a non-integer timeout value: %r' % expire_time)
        cache_key = self.fragment_name
        value = cache.get(cache_key)
        if value is None:
            value = self.nodelist.render(context)
            cache.set(cache_key, value, expire_time)
        return value

def do_clevercache(parser, token):
    nodelist = parser.parse(('endclevercache',))
    parser.delete_first_token()
    tokens = token.contents.split()
    if len(tokens) < 3:
        raise template.TemplateSyntaxError(u"'%r' tag requires at least 2 arguments." % tokens[0])
    return CleverCacheNode(nodelist, tokens[1], tokens[2])
register.tag('clevercache', do_clevercache)


class TreeNode(template.Node):
    def __init__(self, tree, node_list):
        self.tree = tree
        self.node_list = node_list

    def render(self, context):
        tree = self.tree.resolve(context)

        # итератор по входному списку, выдающий пары вида 
        # (элемент списка, его подсписок), причём одного из элемента пары
        # может не быть
        def pairs(items):

            # внутренний "грязный" генератор, выдающий пары, где могут быть
            # бесполезные: с обоими пустыми head и tail
            def dirty(items):
                items = iter(items)
                head = None
                try:
                    while True:
                        item = items.next()
                        if isinstance(item, (list, tuple)):
                            yield head, item
                            head = None
                        else:
                            yield head, None
                            head = item
                except StopIteration:
                    yield head, None

            # фильтр над грязным генератором, удаляющий бесполезные пары
            return ((h, t) for h, t in dirty(items) if h or t)

        # выводит элемент списка с подсписком
        # для подсписка рекурсивно вызывается render_items
        def render_item(item, sub_items, level):
            context.update({'item': item, 'level': level})
            ul_pattern = '<ul>%s</ul>'
            return ''.join([
                item and self.node_list.render(context) or '',
                sub_items and ul_pattern % ''.join(render_items(sub_items, level + 1)) or '',
                '</li>',
            ])

        # вывод списка элементов
        def render_items(items, level):
            return ''.join(render_item(h, t, level) for h, t in pairs(items))

        return render_items(tree, 0)

@register.tag
def tree(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError('"%s" takes one argument: tree-structured list' % bits[0])
    node_list = parser.parse('end' + bits[0])
    parser.delete_first_token()
    return TreeNode(parser.compile_filter(bits[1]), node_list)

@register.filter
def astree(items, attribute):

    # перевод списка в dict: parent -> список детей
    parent_map = defaultdict(list)
    for item in items:
        try:
            attr_val = getattr(item, attribute)
        except:
            attr_val = None
        parent_map[attr_val].append(item)

    # рекурсивный вывод детей одного parent'а
    def tree_level(parent):
        for item in parent_map[parent]:
            yield item
            sub_items = list(tree_level(item))
            if sub_items:
                yield sub_items
    try:
        #first_item = items[0].parent
        first_item = getattr(items[0], attribute)
    except:
        first_item = None
    return list(tree_level(first_item))

@register.inclusion_tag('common_paginator.html')
def paginator(objects, request=None):
    if request:
        query = request.GET.copy()
        query.update(request.POST.copy())
        try:
            del query['page']
        except:
            pass
    return {'objects': objects, 'query': '&'+query.urlencode()}

@register.filter
def morph(value, arg):
    # У меня есть ('1 пчела', '2 пчелы', '5 пчел')
    CASES = (2, 0, 1, 1, 1, 2)
    try:
        value = int(value)
    except:
        return ''
    titles = map(lambda x: x.strip(), arg.split(','))[:3]
    while len(titles) < 3:
        titles.append(titles[0])
    if (value % 100 > 4 and value % 100 < 20):
        return titles[2]
    return titles[CASES[min(value % 10, 5)]]

@register.filter
def split(value, sep=None):
    sep = sep or ','
    return value.split(sep)

@register.filter
def items_in_group(value, groups):
    return int(math.ceil(float(len(value)) / int(groups)))
    
@register.filter
def to_array(value):
    return [value]

@register.filter
def format1000(s, tSep=' ', dSep='.'):
    '''Splits a general float on thousands. GIGO on general input'''
    if s == None:
        return 0
    if not isinstance( s, str ):
        s = str( s )
        
    cnt=0
    numChars=dSep+'0123456789'
    ls=len(s)
    while cnt < ls and s[cnt] not in numChars: cnt += 1

    lhs = s[ 0:cnt ]
    s = s[ cnt: ]
    if dSep == '':
        cnt = -1
    else:
        cnt = s.rfind( dSep )
    if cnt > 0:
        rhs = dSep + s[ cnt+1: ]
        s = s[ :cnt ]
    else:
        rhs = ''

    splt=''
    while s != '':
        splt= s[ -3: ] + tSep + splt
        s = s[ :-3 ]

    return lhs + splt[ :-1 ] + rhs

@register.filter
def rus_full_date(value):
    try:
        return u"%d %s %d" % (value.day, settings.MONTHS[value.month], value.year)
    except:
        return value

@register.filter
def rus_full_datetime(value):
    try:
        return u"%d %s %d %s" % (value.day, settings.MONTHS[value.month], value.year,
                                    value.strftime('%H:%M'))
    except:
        return value    
        
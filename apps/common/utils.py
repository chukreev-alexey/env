# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from settings import MONTHS

def get_paginator(request, queryset, rows_on_page=None, pages_forward=None):
    DEFAULT_ROWS_ON_PAGE = 30
    DEFAULT_PAGES_FORWARD = 5
    rows_on_page = rows_on_page or DEFAULT_ROWS_ON_PAGE
    pages_forward = pages_forward or DEFAULT_PAGES_FORWARD 
    
    paginator = Paginator(queryset, rows_on_page, orphans=0)
    try:
        page = int(request.REQUEST.get('page', '1'))
    except ValueError:
        page = 1
    try:
        objects = paginator.page(page)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)
    
    start_index = page - (pages_forward+1)
    if start_index < 0:
       start_index = 0
    objects.paginator.slice = "%d:%d" % (start_index, page+pages_forward)
    return objects

def get_int_key(arr, key):
    if arr.get(key, False):
        try:
            return int(arr[key])
        except:
            pass
    return False    
    
def intlist(arr):
    for item in arr:
        try:
            yield int(item)
        except:
            pass

def rus_date(value):
    return u"%d %s" % (value.day, MONTHS[value.month])

def rus_full_date(value):
    return u"%d %s %d" % (value.day, MONTHS[value.month], value.day)

ORDER_VAR = 'sort'
ORDER_TYPE_VAR = 'stype'
class SortHeaders:
    """
    Handles generation of an argument for the Django ORM's
    ``order_by`` method and generation of table headers which reflect
    the currently selected sort, based on defined table headers with
    matching sort criteria.

    Based in part on the Django Admin application's ``ChangeList``
    functionality.
    """
    def __init__(self, request, headers, default_order_field=None,
            default_order_type='asc', additional_params=None):
        """
        request
            The request currently being processed - the current sort
            order field and type are determined based on GET
            parameters.

        headers
            A list of two-tuples of header text and matching ordering
            criteria for use with the Django ORM's ``order_by``
            method. A criterion of ``None`` indicates that a header
            is not sortable.

        default_order_field
            The index of the header definition to be used for default
            ordering and when an invalid or non-sortable header is
            specified in GET parameters. If not specified, the index
            of the first sortable header will be used.

        default_order_type
            The default type of ordering used - must be one of
            ``'asc`` or ``'desc'``.

        additional_params:
            Query parameters which should always appear in sort links,
            specified as a dictionary mapping parameter names to
            values. For example, this might contain the current page
            number if you're sorting a paginated list of items.
        """
        if default_order_field is None:
            for i, (header, query_lookup) in enumerate(headers):
                if query_lookup is not None:
                    default_order_field = i
                    break
        if default_order_field is None:
            raise AttributeError('No default_order_field was specified and none of the header definitions given were sortable.')
        if default_order_type not in ('asc', 'desc'):
            raise AttributeError('If given, default_order_type must be one of \'asc\' or \'desc\'.')
        if additional_params is None: additional_params = {}

        self.header_defs = headers
        self.additional_params = additional_params
        self.order_field, self.order_type = default_order_field, default_order_type

        # Determine order field and order type for the current request
        params = dict(request.GET.items())
        if ORDER_VAR in params:
            try:
                new_order_field = int(params[ORDER_VAR])
                if headers[new_order_field][1] is not None:
                    self.order_field = new_order_field
            except (IndexError, ValueError):
                pass # Use the default
        if ORDER_TYPE_VAR in params and params[ORDER_TYPE_VAR] in ('asc', 'desc'):
            self.order_type = params[ORDER_TYPE_VAR]

    def headers(self):
        """
        Generates dicts containing header and sort link details for
        all defined headers.
        """
        for i, (header, order_criterion) in enumerate(self.header_defs):
            th_class = ''
            new_order_type = 'asc'
            if i == self.order_field:
                th_class = '%sending' % self.order_type
                new_order_type = {'asc': 'desc', 'desc': 'asc'}[self.order_type]
            yield (order_criterion or i, {
                'text': header,
                'sortable': order_criterion is not None,
                'url': self.get_query_string({ORDER_VAR: i, ORDER_TYPE_VAR: new_order_type}),
                'class_attr': (th_class or ''),
            })

    def get_query_string(self, params):
        """
        Creates a query string from the given dictionary of
        parameters, including any additonal parameters which should
        always be present.
        """
        params.update(self.additional_params)
        return '?%s' % '&amp;'.join(['%s=%s' % (param, value) \
                                     for param, value in params.items()])

    def get_order_by(self):
        """
        Creates an ordering criterion based on the current order
        field and order type, for use with the Django ORM's
        ``order_by`` method.
        """
        return '%s%s' % (
            self.order_type == 'desc' and '-' or '',
            self.header_defs[self.order_field][1],
        )    
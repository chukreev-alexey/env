# -*- coding: utf-8 -*-
import re
from operator import attrgetter
from shop.models import Product
from common.templatetags.common_tags import morph, format1000
from django.utils import simplejson

REG_CART_ITEMS = re.compile(r'cart-?\d+')

class Cart(object):
    def __init__(self, request, init=False, prefix='cart'):
        self.prefix = u'%s-' % prefix
        self.REG_CART_ITEMS = re.compile(r'%s?\d+' % self.prefix)
        self.i = 0
        self.cart_text = ''
        self.count = 0
        self.all_sum_text = ''
        self.one_sum_text = ''
        self.request = request
        #self.request.session['cart-115'] = {'product': 115, 'amount': 1}
        #self.request.session['cart-25'] = {'product': 25, 'amount': 2}
        if init:
            self._calculate()
    
    def __unicode__(self):
        return self.cart_text
    
    def _calculate(self, product=None):
        self.objects = []
        self.all_sum = 0
        self.one_sum = 0
        self.count = 0
        """
        
        key_list = self.key_list()
        
        null_item_list = filter(lambda x: self.request.session[x]['amount'] == 0, key_list)
        for item in null_item_list:
            try:
                key_list.remove(item)
            except ValueError:
                pass
            try:
                del self.request.session[item]
            except KeyError:
                pass
        cart_dic = dict(map(lambda x: tuple(self.request.session[x].values()), self.key_list()))
        
        
        self.count = sum(cart_dic.values())
        
        cart_items = ProductPrice.objects.filter(pk__in=cart_dic.keys())
        
    
        #for key in self.cart_items:
        """
        for key in self.key_list():
            try:
                data = self.request.session[key]
                cart_item = Product.objects.get(pk=int(data['product']))
            except:
                self.delete(key, is_recalc=False)
                continue
            cart_item.amount = int(data['amount'])
            if cart_item.amount <= 0:
                self.delete(key, is_recalc=False)
                continue
            price = cart_item.price
            if data['product'] == product and product:
                self.one_sum = price * cart_item.amount
            cart_item.sum_price = price * cart_item.amount
            self.all_sum += cart_item.sum_price
            self.count += cart_item.amount
            self.objects.append(cart_item)
        
        self.objects = self.sort_list(self.objects)
        self.product_id_list = set(map(lambda x: x.id, self.objects))
        if self.count > 0:
            self.cart_text = u'В корзине %d %s<br />на сумму %s %s' % \
                             (self.count,
                              morph(self.count, u"товар,товара,товаров"),
                              format1000(self.all_sum),
                              morph(self.all_sum, u"рубль,рубля,рублей"))
        else:
            self.cart_text = u'Ваша корзина пуста'
            
        self.one_sum_text = "%s %s" % \
            (format1000(self.one_sum), morph(self.one_sum, u"рубль,рубля,рублей"))
        self.all_sum_text = "%s %s" % \
            (format1000(self.all_sum), morph(self.all_sum, u"рубль,рубля,рублей"))
            
    def sort_list(self, uslist):
        return sorted(uslist, key=attrgetter('sort', 'name', 'price'))
    
    def serialize(self):
        return simplejson.dumps({
            'cart_text': self.cart_text,
            'count': self.count,
            'all_sum':  float(self.all_sum),
            'all_sum_text': self.all_sum_text,
            'one_sum':  float(self.one_sum),
            'one_sum_text': self.one_sum_text,
            'i': self.i,
        })
    
    def get_cart_id(self, key):
        return '%s%s' % (self.prefix, key)
    
    def get_cart_key(self, id):
        return id.replace(self.prefix, '')
    
    def add(self, key):
        cart_id = self.get_cart_id(key)
        try:
            amount = int(self.request.session[cart_id]['amount'])
        except:
            amount = 0
        self.request.session[cart_id] = {'product'  : key,
                                         'amount'   : amount + 1}
        self._calculate()
    
    def update(self, data):
        cart_id = self.get_cart_id(data['product'])
        self.request.session[cart_id] = {'product'  : data['product'],
                                         'amount'   : data['amount']}
        self._calculate(data['product'])
    
    def delete(self, id, is_recalc=True):
        cart_id = self.get_cart_id(id)
        try:
            del self.request.session[cart_id]
        except KeyError:
            pass
        if is_recalc:
            self._calculate()

    def delete_all(self):
        for id in self.key_list():
            self.delete(self.get_cart_key(id))
    
    def key_list(self):
        return filter(
            lambda x: self.REG_CART_ITEMS.match(x),
            self.request.session.keys()
        )
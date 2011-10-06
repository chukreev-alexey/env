# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.template import RequestContext
from django.template.loader import render_to_string

from common.fields import emails_list
from cart import Cart
from shop.forms import OrderForm


def show_cart(request):
    return render_to_response('cart.html', {},
        context_instance=RequestContext(request))

def order_cart(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            subject = u'Заказ с сайта'
            recipients = []
            try:
                recipients.extend(emails_list(request.settings.email))
            except:
                recipients.append(settings.ADMINS[0][1])
            cart = Cart(request, init=True)
            letter_context = form.cleaned_data
            letter_context.update({'site': request.settings.project})
            order_text = render_to_string('order_info.txt', {'cart': cart})
            letter_content = render_to_string('order_letter.txt', letter_context)
            letter_content += order_text
            send_mail(subject, letter_content, letter_context['email'] or recipients[0], recipients)
            success_message = u"""
            Благодарим за то, что Вы воспользовались услугами нашего Интернет-магазина.
            Ваша заявка принята в обработку и наш менеджер свяжется с Вами в ближайшее время для уточнения деталей.
            Мы будем благодарны Вам, если Вы оставите на нашем сайте свой отзыв о работе нашего  Интернет-магазина.
            """
            messages.add_message(request, messages.SUCCESS, success_message)
            cart.delete_all()
            return HttpResponseRedirect('')
    else:
        form = OrderForm()
    return render_to_response('cart_order.html', {'form': form},
        context_instance=RequestContext(request))   
        
def add_cart(request):
    cart = Cart(request)
    product = int(request.POST.get('product', 0))
    if product > 0:
        request = cart.add(product)
    return HttpResponse(cart.serialize())
    
def update_cart(request):
    cart = Cart(request)
    product = int(request.POST.get('product', '0'))
    amount = int(request.POST.get('amount', '0'))
    i = int(request.POST.get('i', '0'))
    data = None
    if product > 0 and amount > 0:
        cart.update({'product': product, 'amount': amount})
        cart.i = i
        return HttpResponse(cart.serialize())
    else:
        raise Http404

def delete_cart(request, id):
    cart = Cart(request)
    cart.delete(id)
    if request.META.get('HTTP_X_REQUESTED_WITH', '') == 'XMLHttpRequest':
        return HttpResponse(cart.serialize())
    else:
        return redirect(reverse('show_cart'))

def empty_cart(request):
    cart = Cart(request)
    cart.delete_all()
    return redirect('/') 
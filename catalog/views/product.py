from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.http import HttpResponseRedirect
from django import forms
from catalog.models import Category as ccmod
from catalog imports models as cmod

@view_function
def process_request(request, product:cmod.Product):
    if product == None:
        cats1 = ccmod.objects.all()
        context = {
            'cats': cats1
        }
        return request.dmp.render('index.html', context)
    else:
        prod1 = pmod.objects.filter(id=product.id)

        cats1 = ccmod.objects.all()
        context = {
            'cats': cats1,
            'prod': prod1
        }
        return request.dmp.render('product.html', context)

@view_function
def tile(request, product:cmod.Product):
    return request.dmp.render('product.tile.html', {
        'product': product,
    })
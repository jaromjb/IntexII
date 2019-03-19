from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.http import HttpResponseRedirect
from django import forms
from catalog.models import Category as ccmod
from catalog import models as cmod
from catalog.models import Product as pmod
from django.conf import settings


@view_function
def process_request(request, product:cmod.Product):
    if product == None:
        cats1 = ccmod.objects.all()
        context = {
            'cats': cats1,
        }
        return request.dmp.render('index.html', context)
    else:
        cats1 = ccmod.objects.all()
        images = product.image_urls()
        context = {
            'cats': cats1,
            'product': product,
            'images': images,
        }
        return request.dmp.render('product.html', context)
        
@view_function        
def tile(request, product:cmod.Product):
    context = {
        'product': product,
    }
    return request.dmp.render('product.tile.html', context)
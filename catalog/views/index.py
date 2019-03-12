from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from catalog.models import Product as pmod
from django.http import HttpResponseRedirect
from django import forms
from catalog.models import Category
import math

ITEMS_PER_PAGE = 3

@view_function
def process_request(request, category:cmod.Category=None, page:int=1):
    products = cmod.Product.objects.filter(status="A")
    if category is not None:
        products = products.filter(category = category)
        
    products = products[(page - 1) * ITEMS_PER_PAGE: page * ITEMS_PER_PAGE]

    return request.dmp.render('index.html', {
        'category': category,
        'products': products,
        'page': page,
        'numpages': math.ceil(products.count() /  ITEMS_PER_PAGE),
    })



    nc = cmod.Category()
    nc.name = 'Food'
    nc.save()

    nc = cmod.Category()
    nc.name = 'Clothing'
    nc.save()

    nc = cmod.Category()
    nc.name = 'Instruments'
    nc.save()

    #np = pmod()
    #np.category
    
    
    return request.dmp.render('index.html', context)


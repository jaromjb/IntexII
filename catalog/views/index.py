from django.conf import settings
from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.http import HttpResponseRedirect
from django import forms
from catalog import models as cmod
from catalog.models import Category as ccmod
from catalog.models import Product as pmod
import math

ITEMS_PER_PAGE = 8
@view_function
def process_request(request, category:cmod.Category=None, page:int=1):
    if category == None:
        prod1 = pmod.objects.filter(status="A")
    else:
        prod1 = pmod.objects.filter(category=category.id, status="A")
        
    prod2 = prod1[(page - 1) * ITEMS_PER_PAGE: page * ITEMS_PER_PAGE]
    cats1 = ccmod.objects.all()
    context = {
        'cats': cats1,
        'prods': prod2,
        'page': page,
        'numpages': math.ceil(prod1.count() / ITEMS_PER_PAGE),
        'category': category,
    }
    return request.dmp.render('index.html', context)
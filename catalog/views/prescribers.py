from django.conf import settings
from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.http import HttpResponseRedirect
from django import forms
from catalog import models as cmod
from catalog.models import Category as ccmod
from catalog.models import Product as pmod
from catalog.models import Prescribers as ppmod
import math

ITEMS_PER_PAGE = 50
@view_function
def process_request(request, page:int=1):
    
        
    
    presc = ppmod.objects.all()
    presc1 = presc[(page - 1) * ITEMS_PER_PAGE: page * ITEMS_PER_PAGE]
    context = {
        
        'page': page,
        'numpages': math.ceil(presc.count() / ITEMS_PER_PAGE),
        'presc': presc1,
    }
    return request.dmp.render('prescribers.html', context)
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
from catalog.models import Opioids as omod
from django.db.models import Q

ITEMS_PER_PAGE = 50
@view_function
def process_request(request, page:int=1):
    if request.user.is_authenticated:

        drugs = omod.objects.all()
        search_term = ''

        if 'search' in request.GET:
            search_term = request.GET['search']
            drugs = drugs.filter(Q(drugName__icontains=search_term) | Q(isOpioid__icontains=search_term)) 
        
        drugs1 = drugs[(page - 1) * ITEMS_PER_PAGE: page * ITEMS_PER_PAGE]
        context = {
            
            'page': page,
            'numpages': math.ceil(drugs.count() / ITEMS_PER_PAGE),
            'drugs': drugs1,
        }
        return request.dmp.render('drugs.html', context)
    else:
        return HttpResponseRedirect("/account/login")
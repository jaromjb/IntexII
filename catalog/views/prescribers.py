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
from django.db.models import Q
import requests

ITEMS_PER_PAGE = 50
@view_function
def process_request(request, page:int=1):
    if request.user.is_authenticated:

        presc = ppmod.objects.all()
        search_term = ''

        if 'search' in request.GET:
            search_term = request.GET['search']
            presc = presc.filter(Q(doctorID__icontains=search_term) | Q(fName__icontains=search_term) | Q(lName__icontains=search_term) | Q(gender__icontains=search_term)| Q(credentials__icontains=search_term) | Q(state__icontains=search_term) | Q(specialty__icontains=search_term)) 
        
        presc1 = presc[(page - 1) * ITEMS_PER_PAGE: page * ITEMS_PER_PAGE]
        context = {            
            'page': page,
            'numpages': math.ceil(presc.count() / ITEMS_PER_PAGE),
            'presc': presc1,
            'search_term':search_term,
        }
        return request.dmp.render('prescribers.html', context)
    else:
        return HttpResponseRedirect("/account/login")
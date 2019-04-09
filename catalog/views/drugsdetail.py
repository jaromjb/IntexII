from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.http import HttpResponseRedirect
from django import forms
from catalog.models import Category as ccmod
from catalog import models as cmod
from catalog.models import Product as pmod
from django.conf import settings
from catalog.models import Prescribers as ppmod
from catalog.models import Triple as tmod
import psycopg2
from catalog.models import Opioids as omod


@view_function
def process_request(request, opioids:cmod.Opioids):    

   
    topPrescribers =[]
    drugs = []
    triple = tmod.objects.all()    
    topPrescribers = cmod.Triple.objects.filter(drug = opioids.drugName).order_by('qty')[:10]
    triple = tmod.objects.all()
    value = opioids.isOpioid
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = cartForm(request.POST)
        form.product = product
        form.user = request.user
        # check whether it's valid:
        if form.is_valid():
            si = cmod.SaleItem()
            si.sale = request.user.get_shopping_cart()
            si.product = product
            si.quantity = form.cleaned_data.get('quantity')
            si.price = product.price
            si.save()
            return HttpResponseRedirect("/catalog/cart")
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:        
    #GET
    else:
        form = cartForm()                
    context={       
        #'prescribers':prescribers,
        'form':form,
        'topPrescribers':topPrescribers,
        'triple':triple,
        'opioids': opioids,
        'omod':omod,
        'value':value,
        'drugs':drugs,
    }
    return request.dmp.render('drugsdetail.html', context)

    

class cartForm(forms.Form):
    quantity = forms.IntegerField(label="Quantity", min_value=0)

@view_function        
def tile(request, product:cmod.Product):
    context = {
        'product': product,        
    }
    return request.dmp.render('product.tile.html', context)
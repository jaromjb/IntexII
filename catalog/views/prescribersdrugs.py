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
import http.client
import requests


@view_function
def process_request(request, prescribers:cmod.Prescribers, triple:cmod.Triple, drugs):    
    if request.user.is_authenticated:
        
        newdrug = []
        
        qtyPrescribed = cmod.Prescribers.objects.filter(doctorID = triple.doctorID)     
       
        
        context={       
            'prescribers':prescribers,
            'newdrug':newdrug,
            'qtyPrescribed':qtyPrescribed,
        }


        return request.dmp.render('prescribersdrugs.html', context)
    else:
        return HttpResponseRedirect("/account/login")



class cartForm(forms.Form):
    quantity = forms.IntegerField(label="Quantity", min_value=0)

@view_function        
def tile(request, product:cmod.Product):
    context = {
        'product': product,        
    }
    return request.dmp.render('product.tile.html', context)
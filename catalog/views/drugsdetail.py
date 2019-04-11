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
import requests

@view_function
def process_request(request, opioids:cmod.Opioids):    

    if request.user.is_authenticated:

        listdrugs=cmod.Triple.objects.filter(drug=opioids.id).order_by('-qty')[:10]
        prescribers = cmod.Prescribers.objects.all()

        topPrescribers =[]
        drugs = []
        triple = tmod.objects.all()    
        #topPrescribers = cmod.Prescribers.objects.filter(drug = opioids.drugName).order_by('qty')[:10]
        triple = tmod.objects.all()
        value = opioids.isOpioid

        url = "https://ussouthcentral.services.azureml.net/workspaces/807deeba78eb4852b9eb668561bb0ef8/services/98c40a2ed7ae45feb771712d085b6e07/execute"

        querystring = {"api-version":"2.0","details":"true"}

        payload = "{\r\n  \"Inputs\": {\r\n    \"input1\": {\r\n      \"ColumnNames\": [\r\n        \"Id\",\r\n        \"DoctorID\",\r\n        \"Fname\",\r\n        \"Lname\",\r\n        \"Gender\",\r\n        \"State\",\r\n        \"Credentials\",\r\n        \"Specialty\",\r\n        \"Opioid.Prescriber\",\r\n        \"TotalPrescriptions\"\r\n      ],\r\n      \"Values\": [\r\n        [\r\n          \"0\",\r\n          \"0\",\r\n          \"value\",\r\n          \"value\",\r\n          \"value\",\r\n          \"value\",\r\n          \"value\",\r\n          \"value\",\r\n          \"0\",\r\n          \"0\"\r\n        ]\r\n      ]\r\n    }\r\n  },\r\n  \"GlobalParameters\": {}\r\n}"
        headers = {
            'Authorization': "Bearer umVWLr3LDvFrZKIR9eOMv8U10mM+d1APjOFJQWNfa8QVl6kRWk2+usTqd8PRSI5v7jSTPsOmCAECXIMHUPJaQQ==",
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "eb9ddd44-121f-4dc1-adcf-fee1f88c914b"
            }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

        print(response.text)
        
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
            'prescribers':prescribers,
            'value':value,
            'drugs':drugs,
            'listdrugs':listdrugs,
        }
        return request.dmp.render('drugsdetail.html', context)
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
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
def process_request(request, prescribers:cmod.Prescribers):    
    if request.user.is_authenticated:
 
        drugs =[]
        
        drugs = cmod.Triple.objects.filter(doctorID = prescribers.doctorID).order_by('qty')[:10]
        triple = tmod.objects.all()
        
        url = "https://ussouthcentral.services.azureml.net/workspaces/807deeba78eb4852b9eb668561bb0ef8/services/21a1090cc4fc41f9b11aeab5702e9f87/execute"

        querystring = {"api-version":"2.0","details":"true"}

        payload = "{\r\n  \"Inputs\": {\r\n    \"input1\": {\r\n      \"ColumnNames\": [\r\n        \"prescribers.id\",\r\n        \"prescribers.doctorID\",\r\n        \""+ prescribers.fName +"\",\r\n        \""+ prescribers.lName +"\",\r\n        \""+ prescribers.gender +"\",\r\n        \""+ prescribers.state +"\",\r\n        \""+ prescribers.credentials + "\",\r\n        \""+ prescribers.specialty + "\",\r\n        \"prescribers.opioid_prescriber\",\r\n        \"prescribers.totalPrescriptions\"\r\n      ],\r\n      \"Values\": [\r\n        [\r\n          \"0\",\r\n          \"0\",\r\n          \"value\",\r\n          \"value\",\r\n          \"value\",\r\n          \"value\",\r\n          \"value\",\r\n          \"value\",\r\n          \"0\",\r\n          \"0\"\r\n        ]\r\n      ]\r\n    }\r\n  },\r\n  \"GlobalParameters\": {}\r\n}"
        headers = {
            'Authorization': "Bearer 1gngtevU4h0YBW58WJvNM7n13VkJs2WTIrMU2F7+eQLbiHJo5NjXijclBi/dTk8am6nhRjQpJzXQZwifCCAx9g==",
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "0cb58e05-0b65-46ea-af30-849998a2e4f3"
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
            'prescribers':prescribers,
            'form':form,
            'drugs':drugs,
            'triple':triple,
        }


        return request.dmp.render('prescribersdetail.html', context)
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
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
def process_request(request, prescriberID=int):    
    if request.user.is_authenticated:
        
        pid = prescriberID
        p=cmod.Prescribers.objects.get(doctorID=prescriberID)

        drugs =[]
        drugs = cmod.Triple.objects.filter(doctor = pid).order_by('-qty')[:10]
        #triple = tmod.objects.filter(doctor = prescriberID)
        #value = opioid_prescriber
        
        
        url = "https://ussouthcentral.services.azureml.net/workspaces/807deeba78eb4852b9eb668561bb0ef8/services/21a1090cc4fc41f9b11aeab5702e9f87/execute"

        querystring = {"api-version":"2.0","details":"true"}

        #payload = "{\r\n  \"Inputs\": {\r\n    \"input1\": {\r\n      \"ColumnNames\": [\r\n        \"prescribers.id\",\r\n        \"prescribers.doctorID\",\r\n        \""+ prescribers.fName +"\",\r\n        \""+ prescribers.lName +"\",\r\n        \""+ prescribers.gender +"\",\r\n        \""+ prescribers.state +"\",\r\n        \""+ prescribers.credentials + "\",\r\n        \""+ prescribers.specialty + "\",\r\n        \"prescribers.opioid_prescriber\",\r\n        \"prescribers.totalPrescriptions\"\r\n      ],\r\n      \"Values\": [\r\n        [\r\n          \"0\",\r\n          \"0\",\r\n          \"value\",\r\n          \"value\",\r\n          \"value\",\r\n          \"value\",\r\n          \"value\",\r\n          \"value\",\r\n          \"0\",\r\n          \"0\"\r\n        ]\r\n      ]\r\n    }\r\n  },\r\n  \"GlobalParameters\": {}\r\n}"
        headers = {
            'Authorization': "Bearer 1gngtevU4h0YBW58WJvNM7n13VkJs2WTIrMU2F7+eQLbiHJo5NjXijclBi/dTk8am6nhRjQpJzXQZwifCCAx9g==",
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "0cb58e05-0b65-46ea-af30-849998a2e4f3"
            }

        #response = str(requests.request("POST", url, data=payload, headers=headers, params=querystring))

       # print(response)

        
        context={       
            #'prescribers':prescribers,
            'drugs':drugs,
            #'triple':triple,
            'pid': pid,
            'p':p,
            #'value':value,
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
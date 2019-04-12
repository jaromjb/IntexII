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
import json

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

        url = "https://ussouthcentral.services.azureml.net/workspaces/4328226122df4cf8be6a08eed8f2b3ce/services/a0801176f7074a80a9091ac2efe5bbe4/execute"

        querystring = {"api-version":"2.0","details":"true%0A%0A%0A"}

        payload = "{\r\n  \"Inputs\": {\r\n    \"input1\": {\r\n      \"ColumnNames\": [\r\n        \"DoctorID\",\r\n        \"Drug\",\r\n        \"Qty\"\r\n      ],\r\n      \"Values\": [\r\n        [\r\n          \"0\",\r\n          \""+ opioids.drugName +"\",\r\n          \"0\"\r\n        ]\r\n      ]\r\n    }\r\n  },\r\n  \"GlobalParameters\": {}\r\n}"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer MNo9jE03VcpAcoeiZaBpKll9KDzekj+oY8UL8kop3+/0uyhK/5f1jp0Iy5/Bw/rCM1fxWvPtjvPmqxHrm7R/QA==",
            'cache-control': "no-cache",
            'Postman-Token': "4b7d7f73-2c4a-41d0-98ea-d2c30b918792"
            }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        print("__>>>>>>>")
        print(response.text)

        recommender=response.text

        parsed_json = json.loads(recommender)
        
        prediction=parsed_json["Results"]["output1"]["value"]["Values"]
        prediction=str(prediction)
        prediction=prediction.replace("[", "").replace("]", "").replace("\'", "").replace(" ","")
        prediction=prediction.split(",")
        
        rec=[]
        for item in prediction:
            if item!=opioids.drugName:
                recp=cmod.Opioids.objects.get(drugName=item)
                rec.append(recp)
        recommender=rec
        
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
            'recommender':recommender,
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
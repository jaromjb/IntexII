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
import json

@view_function
def process_request(request, doctorID=int):    
    if request.user.is_authenticated:
        
        pid = doctorID
        p=cmod.Prescribers.objects.get(doctorID=doctorID)

        drugs =[]
        drugs = cmod.Triple.objects.filter(doctor = pid).order_by('-qty')[:10]
        #triple = tmod.objects.filter(doctor = prescriberID)
        #value = opioid_prescriber       
        
       
        url = "https://ussouthcentral.services.azureml.net/workspaces/4328226122df4cf8be6a08eed8f2b3ce/services/95aa126b53374f5487ab51dba899e180/execute"

        querystring = {"api-version":"2.0","details":"true"}

        payload = "{\r\n  \"Inputs\": {\r\n    \"input1\": {\r\n      \"ColumnNames\": [\r\n        \"DoctorID\",\r\n        \"Drug\",\r\n        \"Qty\"\r\n      ],\r\n      \"Values\": [\r\n        [\r\n          \""+ doctorID +"\",\r\n          \"value\",\r\n          \"0\"\r\n        ]\r\n      ]\r\n    }\r\n  },\r\n  \"GlobalParameters\": {}\r\n}"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer UevIlM8Lj/3C1afRNcpOU4A2BMVHvUQ9Wvq9N5cdTbqy3iEb8c8npVR7VQbdj/oOQg1XQKvSZRl3qYLVTU+N7g==",
            'cache-control': "no-cache",
            'Postman-Token': "57da012c-c1ef-48ea-8a76-efc724b7188f"
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
            if item!=doctorID:
                recp=cmod.Prescribers.objects.get(doctorID=item)
                rec.append(recp)
        recommender=rec

        context={       
            #'prescribers':prescribers,
            'drugs':drugs,
            #'triple':triple,
            'pid': pid,
            'p':p,
            'prediction':prediction,
            'recommender':recommender,
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
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

@view_function
def process_request(request):
    if request.user.is_authenticated:
        return request.dmp.render('index.html')
    else:
        return HttpResponseRedirect("/account/login")
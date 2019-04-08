from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.http import HttpResponseRedirect
from django import forms
from catalog.models import Category as ccmod
from catalog import models as cmod
from catalog.models import Product as pmod
from django.conf import settings


@view_function
def process_request(request, product:cmod.Product):    

    images =[]
    images =product.image_urls()    
    categories = cmod.Category.objects.all()
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
        'images':images,
        'product':product,
        'categories':categories,
        'form':form
    }
    return request.dmp.render('product.html', context)



class cartForm(forms.Form):
    quantity = forms.IntegerField(label="Quantity", min_value=0)

@view_function        
def tile(request, product:cmod.Product):
    context = {
        'product': product,
    }
    return request.dmp.render('product.tile.html', context)
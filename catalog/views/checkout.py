from django.conf import settings
from django_mako_plus import view_function, jscontext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from django import forms
from catalog import models as cmod
from decimal import Decimal

@view_function
def process_request(request):
    #process the form
    sale = request.user.get_shopping_cart()
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        form.request = request
        if form.is_valid():            
            return HttpResponseRedirect('/catalog/receipt/{sale.id}')
    else: #GET
        form = CheckoutForm()

    #render the template
    context={
        'sale': sale,
        'form': form,
    }

    return request.dmp.render('checkout.html', context)

class CheckoutForm(forms.Form):
    address = forms.CharField(label='Shipping Address')
    city = forms.CharField(label="Shipping City")
    state = forms.CharField(label='Shipping State')
    zipcode = forms.CharField(label="Shipping Zip")
    stripeToken = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        try:
            sale = self.request.user.get_shopping_cart()
            sale.finalize(self.cleaned_data['stripeToken'])
        except Exception as e:
            raise forms.ValidationError('Error processing payment: {}'.format(e))
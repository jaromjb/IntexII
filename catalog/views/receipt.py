from django.conf import settings
from django.contrib.auth.decorators import login_required
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
import math
import random

@view_function
def process_request(request):
    cart = request.user.get_shopping_cart()
    si = cmod.SaleItem.objects.filter(sale=cart)

    context = {
        'cart': cart,
        'si': si
    }

    return request.dmp.render('receipt.html', context)


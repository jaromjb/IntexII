from django.contrib.auth.models import AbstractUser
from django.db import models
from catalog import models as cmod

# Create your models here.
class User(AbstractUser):
    birthdate = models.DateTimeField(null=True)
    favcolor = models.TextField(null=True)
    def get_shopping_cart(self):
        cart = cmod.Sale.objects.filter(user=self, purchased=None).first()
        if cart is None:
            cart = cmod.Sale()
            cart.user = self
        cart.recalculate()
        cart.save()
        return cart

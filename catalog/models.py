from django.db import models
from django import forms
from django.conf import settings
from decimal import Decimal
import stripe
from datetime import datetime

TAX_RATE = Decimal("0.05")

class Prescribers(models.Model):
    doctorID = models.IntegerField(primary_key=True)
    fName = models.TextField()
    lName = models.TextField()
    gender = models.TextField(max_length=1, default='O',
       choices=(
       ('M', 'Male'),
       ('F', 'Female'),
       ('O', 'Other/Unknown'),
    ),)
    state = models.TextField(max_length=2)
    credentials = models.TextField(null=True)
    specialty = models.TextField()
    opioid_prescriber = models.IntegerField()
    totalPrescriptions = models.IntegerField()

class Overdoses(models.Model):
    state = models.TextField()
    population = models.IntegerField()
    deaths = models.IntegerField()
    abbrev = models.TextField(max_length=2)

class  Opioids(models.Model):  
    drugName = models.TextField()
    isOpioid  = models.IntegerField(choices=(
        ('1', 'Yes'),
        ('0', 'No'),
    ),)

class Triple(models.Model):
    doctor = models.ForeignKey(Prescribers, on_delete=models.CASCADE)
    drug = models.ForeignKey(Opioids, on_delete=models.CASCADE)
    qty = models.IntegerField()

# Create your models here.
class Category(models.Model):
    last_modified = models.DateTimeField(auto_now=True)
    name = models.TextField()

class Product(models.Model):
    choices1 = {
    ('A', 'Active'),
    ('I', 'Inactive')
    }   
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.TextField(db_index=True, choices= choices1, default="A")
    name = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.IntegerField()
    reorder_trigger = models.IntegerField()
    reorder_quantity = models.IntegerField()

    def image_url(self): 
        return self.image_urls()[0]
    def image_urls(self): 
        pimages = ProductImage.objects.filter(product=self)
        urls = []
        for b in pimages:
            urls.append(b.image_url())
        if urls != 0:
            return urls
        else:
            return settings.STATIC_URL + "catalog/media/products/notfound.jpg"

class ProductImage(models.Model):
    filename = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def image_url(self):
        return settings.STATIC_URL + "catalog/media/products/" + self.filename

class Sale(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    purchased = models.DateTimeField(null=True, default=None)
    subtotal = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal(0))
    tax = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal(0))
    total = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal(0))
    charge_id = models.TextField(null=True, default=None) #successful charge id from stripe
    
    def recalculate(self):
       '''Recalculates the subtotal, tax, and total fields. Does not save the object.'''
       rTotal = 0
       rTax = 0
       rSubtotal = 0
       oItems = SaleItem.objects.filter(sale=self, status='A')

       for items in oItems:
           rSubtotal += (items.price * items.quantity)
           
       rTax = rSubtotal * TAX_RATE
       rTotal = rTax + rSubtotal
       self.tax = rTax
       self.subtotal = rSubtotal
       self.total = rTotal

    def finalize(self, stripeToken):        
        '''Finalizes the sale'''
        Items = SaleItem.objects.filter(sale=self, status='A')

        if self.purchased is not None:
            raise ValueError('This sale has already been finalized')

        for item in Items:
            if item.product.quantity < item.quantity:
                raise ValueError(str(item.product.name) + ' only has ' + str(item.product.quantity) + ' available.')

        self.recalculate()

        charge = stripe.Charge.create(
            amount=int(self.total * 100),
            currency='usd',
            description='Example charge',
            source=stripeToken,
        )

        self.purchased = datetime.now()
        self.charge_id = charge['id'] 

        for item in Items:
            item.product.quantity = item.product.quantity - item.quantity

        self.save()

    

class SaleItem(models.Model):
    STATUS_CHOICES = [
        ( 'A', 'Active' ),
        ( 'D', 'Deleted' ),
    ]
    status = models.CharField(max_length=1, default=STATUS_CHOICES[0][0], choices=STATUS_CHOICES)
    sale = models.ForeignKey("Sale", on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey("Product", on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal(0))
    class Meta:
        ordering = [ 'product__name' ]
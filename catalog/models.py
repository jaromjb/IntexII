from django.db import models
from django import forms

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
        return self.images_url()[0]
        # return an absolute URL to the first image for this product, 
        # or if no ProductImage records, the "no image available" image. The return will be something like: `settings.STATIC_URL + "catalog/media/products/rustic-violin.jpg"`
    def images_url(self): 
        pimages = ProductImage.objects.filter(product=self)
        urls = []
        for b in pimages:
            urls.append(b.image_url)
        if urls.count == 0:
            return('settings.STATIC_URL' + "catalog/media/products/notfound.jpg")
        else:
            return urls

        # return a list of absolute URLs to the images for this product, 
        # or if no ProductImage records, a list of one item: the "no image available" image.

class ProductImage(models.Model):
    filename = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def image_url(self):
        return('settings.STATIC_URL' + "catalog/media/products/" + self.filename) 
        # return an absolute URL to this image. 
        # The return will be something like: `settings.STATIC_URL + "catalog/media/products/rustic-violin.jpg"`
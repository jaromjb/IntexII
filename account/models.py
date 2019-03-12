from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    birthdate = models.DateTimeField(null=True)
    favcolor = models.TextField(null=True)
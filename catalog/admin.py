from django.contrib import admin
from .models import Prescribers
from .models import Opioids
from .models import Overdoses
from .models import *
from account.models import User


# Register your models here.

class PrescribersAdmin(admin.ModelAdmin):
    list_display=('doctorID','fName', 'lName', 'specialty', 'state')
    search_fields = ('doctorID','fName', 'lName', 'specialty', 'state')


admin.site.register(Prescribers, PrescribersAdmin)
admin.site.register(User)

from django import forms
from .models import Prescribers

class PrescribersForm(forms.ModelForm):
    class Meta:
        model = Prescribers
        fields = ['doctorID', 'fName', 'lName', 'gender', 'state', 'credentials', 'specialty', 'opiod_prescriber', 'totalPrescriptions']
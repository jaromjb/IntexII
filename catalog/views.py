from django.shortcuts import render, redirect
from .models import Prescribers
from .forms import PrescribersForm
from django.http import HttpResponseRedirect

def list_prescribers(return):
    return HttpResponseRedirect("/catalog/prescribers")

def create_prescriber(request):
    form = PrescribersForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('list_prescribers')
    
    return render(request, 'prescribers-form.html', {form: form})
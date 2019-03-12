from django.conf import settings
from django_mako_plus import view_function, jscontext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from django import forms

@view_function
def process_request(request):

    #process the form
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(request, user)
            return HttpResponseRedirect('/')
    else: #GET
        form = MyForm()

    #render the template
    return request.dmp.render('login.html', {
        'form': form
    })

class MyForm(forms.Form):
    '''An example form'''
    username = forms.CharField(label='Username')
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def clean(self):
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user is None:
            raise forms.ValidationError('Invalid username or password.')
        return self.cleaned_data
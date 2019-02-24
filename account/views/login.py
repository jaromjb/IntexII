from django.conf import settings
from django_mako_plus import view_function, jscontext

@view_function
def process_request(request):
    form = ...
    context = {
       'form': form,
    }
    return request.dmp.render('login.html', context)



# class LoginForm(forms.Form):
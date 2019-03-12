from django_mako_plus import view_function, jscontext
from django.http import HttpResponse

@view_function
def process_request(request):
    return request.dmp.render('api.html', {})

@view_function #says this is open. Allows funciton to be searched in url
def getdata(request):
    return HttpResponse("hey hey hey");

from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.http import HttpResponseRedirect


@view_function
def process_request(request):
    if request.user.is_authenticated:

        utc_time = datetime.utcnow()
        context = {
            # sent to index.html:
            'utc_time': utc_time,
            # sent to index.html and index.js:
            jscontext('utc_epoch'): utc_time.timestamp(),
        }
        return request.dmp.render('index.html', context)
    else:
        return HttpResponseRedirect("/account/login")

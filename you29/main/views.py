import logging
from django.shortcuts import render_to_response
from django.template import RequestContext

def main_page(request):
    logging.debug("main.views.main_page()")
    variables = RequestContext(request, {
        'user':request.user
    })
    return render_to_response('main/main_page.html', variables)

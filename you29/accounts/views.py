import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import RegistrationForm

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save();
            user = authenticate(username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'])
            if user is not None:
                if user.is_active:
                    login(request, user);
                    return HttpResponseRedirect('%s/' % (request.META['SCRIPT_NAME']))
                else:
                    # return a 'disabled account' error message.
                    return HttpResponseRedirect('%s/accounts/login/' % (request.META['SCRIPT_NAME']))
            else:
                # return an 'invalid login' error message.
                return HttpResponseRedirect('%s/accounts/login/' %(request.META['SCRIPT_NAME']))
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
			'script_name':request.META['SCRIPT_NAME'],	
			'form':form})
    return render_to_response('accounts/register.html',variables)


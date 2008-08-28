import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import RegistrationForm

def logout_page(request):
    logging.debug("accounts.views.logout_page()")
    logout(request)
    return HttpResponseRedirect('/')

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
                    return HttpResponseRedirect('/')
                else:
                    # return a 'disabled account' error message.
                    return HttpResponseRedirect('/accounts/login/')
            else:
                # return an 'invalid login' error message.
                return HttpResponseRedirect('/accounts/login/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form':form})
    return render_to_response('accounts/register.html',variables)


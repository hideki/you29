from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import ContactForm

def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save();
            return render_to_response('contact/contact_sent.html', {
							'script_name':request.META['SCRIPT_NAME']});
    else:        
        form = ContactForm(); # An unbound form
        if request.user.is_authenticated():
            form = ContactForm(initial={'name':request.user.username,'email':request.user.email}); # An unbound form
    return render_to_response('contact/contact.html',
						{
							'script_name':request.META['SCRIPT_NAME'],
						'form':form
						},
            context_instance=RequestContext(request));

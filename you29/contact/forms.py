from django import forms
from django.core.mail import send_mail;

class ContactForm(forms.Form):
    name    = forms.CharField(max_length=255); 
    email   = forms.EmailField();
    message = forms.CharField(widget=forms.Textarea());

    def save(self):
        name  = self.cleaned_data['name'];
        email = self.cleaned_data['email'];
        msg   = self.cleaned_data['message'];
        message = "%s (%s) wrote:\n\n%s" % (name, email, msg);
        recipients = ['webmaster@you29.com'];
        send_mail("Site feedback", message, email, recipients);

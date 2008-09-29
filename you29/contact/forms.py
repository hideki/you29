from django import forms
from django.core.mail import send_mail;

SUBJECT_CHOICES = (
    ('general',    'General enquiry'),
    ('bug',        'Problem report'),
    ('suggestion', 'Suggestion/Comment'),
)


class ContactForm(forms.Form):
    subject  = forms.ChoiceField(choices=SUBJECT_CHOICES, label='Subject')
    name     = forms.CharField(max_length=255, label='Your Name'); 
    email    = forms.EmailField(required=False, label='Email (Optional)');
    comments = forms.CharField(widget=forms.Textarea(), label='Comments');

    def save(self):
        subject = self.cleaned_data['subject'];
        name  = self.cleaned_data['name'];
        email = self.cleaned_data['email'];
        comments   = self.cleaned_data['comments'];
        message = "%s (%s) wrote:\n\n%s" % (name, email, comments);
        recipients = ['webmaster@you29.com'];
        send_mail('Feedback from you29: %s' % subject, message, email, recipients);

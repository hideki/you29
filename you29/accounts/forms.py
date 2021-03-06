import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class RegistrationForm(forms.Form):
    username  = forms.CharField(label='Username', max_length=30)
    email     = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password',
        widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label='Retype Password',
        widget=forms.PasswordInput(render_value=False))

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError(
                'Username can only contain alphanumeric \
                 characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Email is already used.')

    def save(self):
        user = User.objects.create_user(
            username = self.cleaned_data['username'],
            password = self.cleaned_data['password1'],
            email    = self.cleaned_data['email'])
        return user;

from django import forms

class BookmarkSaveForm(forms.Form):
    url   = forms.URLField(label='URL')
    title = forms.CharField(label='Title')
    notes = forms.CharField(label='Notes',
        required=False, widget=forms.Textarea)
    tags  = forms.CharField(label='Tags', required=False)
    share = forms.BooleanField(label='Share', required=False)

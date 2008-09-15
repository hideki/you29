from django import forms

class BookmarkSaveForm(forms.Form):
    title = forms.CharField(label='Summary')
    url   = forms.URLField(label='URL')
    notes = forms.CharField(label='Description',
        required=False, widget=forms.Textarea)
    tags  = forms.CharField(label='Tags', required=False)
    share = forms.BooleanField(label='Share', required=False)

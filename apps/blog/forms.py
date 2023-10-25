from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)
    
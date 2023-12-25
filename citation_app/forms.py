from django import forms

class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'id': 'text-area', 'placeholder': 'Enter your text here...'}), label='')


# forms.py
from django import forms

class ExampleForm(forms.Form):
    q = forms.CharField(
        label='Search Books',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter book title...'})
    )

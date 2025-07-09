from django import forms

class ChangeHCCNumberForm(forms.Form):
    new_hcc_number = forms.CharField(max_length=20, label="New HCC Number", widget=forms.TextInput(attrs={'class': 'form-control'}))

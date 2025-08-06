from django import forms
from .models import ClientCard, ChildICT

class ClientCardForm(forms.ModelForm):
    class Meta:
        model = ClientCard
        fields = ['card_type', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ChildICTForm(forms.ModelForm):
    class Meta:
        model = ChildICT
        fields = ['child_name', 'child_dob', 'hiv_status', 'date_tested', 'notes']
        widgets = {
            'child_dob': forms.DateInput(attrs={'type': 'date'}),
            'date_tested': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
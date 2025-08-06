from django import forms
from .models import ChildVisit

class ChildVisitForm(forms.ModelForm):
    class Meta:
        model = ChildVisit
        fields = '__all__'
        exclude = ['patient']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'next_outcome_date': forms.DateInput(attrs={'type': 'date'}),
        }
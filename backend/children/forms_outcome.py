from django import forms
from .models import ChildVisit

class OutcomeVisitForm(forms.ModelForm):
    class Meta:
        model = ChildVisit
        fields = ['follow_up_outcome', 'next_appointment_or_outcome_date']
        widgets = {
            'follow_up_outcome': forms.Select(attrs={'class': 'form-select'}),
            'next_appointment_or_outcome_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

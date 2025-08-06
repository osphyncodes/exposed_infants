from django import forms
from .models import ChildVisit
from django.core.exceptions import ValidationError
from datetime import date

class ChildVisitForm(forms.ModelForm):
    class Meta:
        model = ChildVisit
        exclude = ['patient']
        widgets = {
            'visit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'visit_type': forms.Select(attrs={'class': 'form-select'}),
            'entry_type': forms.Select(attrs={'class': 'form-select'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'bp': forms.TextInput(attrs={'class': 'form-control'}),
            'side_effects': forms.Select(attrs={'class': 'form-select'}),
            'tab_status': forms.Select(attrs={'class': 'form-select'}),
            'viral_load': forms.Select(attrs={'class': 'form-select'}),
            'pill_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'regimen': forms.TextInput(attrs={'class': 'form-control'}),
            'arv_given': forms.NumberInput(attrs={'class': 'form-control'}),
            'cpt_given': forms.NumberInput(attrs={'class': 'form-control'}),
            'tpt_given' : forms.Select(attrs={'class' : 'form-select'}),
            'tpt_amout': forms.NumberInput(attrs={'class': 'form-control'}),
            'next_outcome_date':forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        visit_date = cleaned_data.get('visit_date')
        next_appointment_date = cleaned_data.get('next_outcome_date')
        
        if visit_date > date.today():
            raise ValidationError("Visit date cannot be greater than today")
        
        if next_appointment_date <= visit_date:
            raise ValidationError("Next Appointment date should be greater that visit date.")

        return cleaned_data

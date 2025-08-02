from django import forms
from .models import Session, Attendance
from pact.models import Patient
from django_select2.forms import ModelSelect2Widget

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['session_date', 'teen_range', 'session_type', 'notes', 'facilitator', 'duration']
        widgets = {
            'session_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PatientSearchWidget(ModelSelect2Widget):
    search_fields = [
        'arv_number__icontains',
        'first_name__icontains',
        'last_name__icontains',
    ]
    
    def label_from_instance(self, obj):
        return f"{obj.arv_number} - {obj.full_name()}"

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['patient','village', 'new_in_teen', 'purpose', 'guardian_present', 'school', 'vl_drawn', 'notes']
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Search patient...'
            }),
            'purpose': forms.Select(attrs={'class': 'form-select'}),
            'school': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'new_in_teen': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'type': 'checkbox',
                'role': 'switch'
            }),
            'guardian_present': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'type': 'checkbox',
                'role': 'switch'
            }),
            'vl_drawn': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'type': 'checkbox',
                'role': 'switch'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.all()
        self.fields['purpose'].choices = [
            ('', 'Select purpose'),
            ('Clinic', 'Clinic'),
            ('Support', 'Support')
        ]
        self.fields['school'].choices = [
            ('', 'Select status'),
            ('No', 'No'),
            ('Yes, Day', 'Yes, Day'),
            ('Yes, BRD', 'Yes, BRD')
        ]
from django import forms
from .models import Child, ChildVisit, HTSSample
from datetime import date
from django.core.exceptions import ValidationError

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = [
            'hcc_number',
            'child_name',
            'child_dob',
            'child_gender',
            'child_birth_weight',
            'guardian_name',
            'relationship',
            'guardian_phone',
            'physical_address',
            'agrees_to_fup',
            'mother_status',
            'mother_art_number',
            'mother_art_start_date',
        ]
        widgets = {
            'hcc_number': forms.TextInput(attrs={'class': 'form-control'}),
            'child_name': forms.TextInput(attrs={'class': 'form-control'}),
            'child_dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'child_gender': forms.Select(attrs={'class': 'form-select'}),
            'child_birth_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'physical_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'agrees_to_fup': forms.Select(attrs={'class': 'form-select'}),
            'mother_status': forms.Select(attrs={'class': 'form-select'}),
            'mother_art_number': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_art_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # hcc_number is not editable, but we can show it as read-only if needed

class ChildVisitForm(forms.ModelForm):
    class Meta:
        model = ChildVisit
        exclude = ['child']
        widgets = {
            'visit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'muac': forms.NumberInput(attrs={'class': 'form-control'}),
            'wasting': forms.Select(attrs={'class': 'form-select'}),
            'breastfeeding': forms.Select(attrs={'class': 'form-select'}),
            'mother_art_status': forms.Select(attrs={'class': 'form-select'}),
            'clinical_monitoring': forms.Select(attrs={'class': 'form-select'}),
            'hiv_testing': forms.Select(attrs={'class': 'form-select'}),
            'infection_status': forms.Select(attrs={'class': 'form-select'}),
            'drug_given': forms.Select(attrs={'class': 'form-select'}),
            'cpt_given': forms.NumberInput(attrs={'class': 'form-control'}),
            'follow_up_outcome': forms.Select(attrs={'class': 'form-select'}),
            'art_number' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'next_appointment_or_outcome_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        visit_date = cleaned_data.get('visit_date')
        next_appointment_date = cleaned_data.get('next_appointment_or_outcome_date')
        infection_status = cleaned_data.get('infection_status')
        follow_up_outcome = cleaned_data.get('follow_up_outcome')

        if not visit_date:
            raise ValidationError('Visit date is a required fied')
        
        if visit_date > date.today():
            raise ValidationError("Visit date cannot be greater than today")
        
        if follow_up_outcome and not next_appointment_date:
            raise ValidationError('Outcome date is required for each selected outcome')
        
        if next_appointment_date <= visit_date:
            raise ValidationError("Next Appointment date should be greater that visit date.")


        return cleaned_data


    def __init__(self, *args, **kwargs):
        self.child = kwargs.pop('child', None)
        super().__init__(*args, **kwargs)
        # Hide weight and muac if child is under 6 months
        if self.child and self.child.child_dob:
            from datetime import date
            visit_date = self.initial.get('visit_date') or date.today()
            # If visit_date is in data, use it
            if 'visit_date' in self.data:
                try:
                    visit_date = self.data['visit_date']
                    visit_date = date.fromisoformat(visit_date)
                except Exception:
                    pass
            age_months = (visit_date.year - self.child.child_dob.year) * 12 + (visit_date.month - self.child.child_dob.month)
            if age_months < 6:
                self.fields.pop('muac', None)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.child:
            instance.child = self.child
        if commit:
            instance.save()
        return instance

class HTSSampleForm(forms.ModelForm):
    class Meta:
        model = HTSSample
        exclude = ['child']
        widgets = {
            'sample_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'test_type': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Select(attrs={'class' : 'form-control'}),
            'sample_id': forms.TextInput(attrs={'class': 'form-control'}),
            'result': forms.Select(attrs={'class': 'form-select'}),
            'date_received': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.child = kwargs.pop('child', None)  # Pull `child` from kwargs
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.child:
            instance.child = self.child
        if commit:
            instance.save()
        return instance
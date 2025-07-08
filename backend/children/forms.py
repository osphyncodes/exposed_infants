from django import forms
from .models import Child, ChildVisit, HTSSample

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
            'cpt_given': forms.NumberInput(attrs={'class': 'form-control'}),
            'follow_up_outcome': forms.Select(attrs={'class': 'form-select'}),
            'next_appointment_or_outcome_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

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
                self.fields.pop('weight', None)
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
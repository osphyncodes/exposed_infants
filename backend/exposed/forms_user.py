
from django import forms
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('superuser', 'Superuser'),
    ('standard', 'Standard'),
]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), label='Role')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        # Set permissions based on role
        role = self.cleaned_data.get('role')
        if role == 'superuser':
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
        if commit:
            user.save()
        return user

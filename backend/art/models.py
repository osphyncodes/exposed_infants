from django.db import models
from pact.models import Patient

class ChildVisit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient')
    visit_date = models.DateField(null=True, blank=True)

    VISIT_TYPE_CHOICES = [
        ('Patient Only', 'Patient Only'),
        ('Guardian Only', 'Guardian Only'),
        ('Both Patient & Guardian', 'Both Patient & Guardian')
    ]
    visit_type = models.CharField(max_length=50, choices=VISIT_TYPE_CHOICES)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


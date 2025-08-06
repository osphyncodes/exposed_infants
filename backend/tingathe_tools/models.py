from django.db import models
from pact.models import Patient # Assuming this is where your ART Patients model is

class ClientCard(models.Model):
    CARD_TYPES = [
        ('HVL', 'HVL Client Card'),
        ('BACK', 'Back to Care Client Card'),
        ('NEW', 'New Initiation Client Card'),
    ]
    
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed Service'),
        ('DIED', 'Died'),
        ('TRANSFERRED', 'Transferred Out'),
        ('STOPPED', 'Treatment Stopped'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=5, choices=CARD_TYPES)
    date_opened = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='IN_PROGRESS')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_card_type_display()} - {self.patient.first_name} {self.patient.last_name}"

class ChildICT(models.Model):
    HIV_STATUS_CHOICES = [
        ('POSITIVE', 'HIV Positive'),
        ('NEGATIVE', 'HIV Negative'),
        ('UNKNOWN', 'Unknown'),
        ('EXPOSED', 'HIV Exposed'),
    ]
    
    mother = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='children')
    child_name = models.CharField(max_length=100)
    child_dob = models.DateField()
    hiv_status = models.CharField(max_length=8, choices=HIV_STATUS_CHOICES, default='UNKNOWN')
    date_tested = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.child_name} - {self.get_hiv_status_display()}"
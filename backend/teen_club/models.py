from django.db import models
from pact.models import Patient
from django.core.validators import MinValueValidator, MaxValueValidator

class Session(models.Model):
    session_date = models.DateField()
    TEEN_RANGE_CHOICES = [
        ('10-19', '10-19')
    ]
    teen_range = models.CharField(max_length=5, choices=TEEN_RANGE_CHOICES)
    SESSION_TYPE = [
        ('Guardian', 'Guardian'),
        ('Teen Only', 'Teen Only')
    ]
    session_type = models.CharField(max_length=9, choices=SESSION_TYPE)
    notes = models.TextField(blank=True, null=True)
    facilitator = models.CharField(max_length=100, blank=True, null=True)
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(240)],
        help_text="Duration in minutes",
        default=60
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session_date', 'teen_range'], name='unique_sessions')
        ]
        ordering = ['-session_date']

    def __str__(self):
        return f"{self.session_date}, Teen Range: {self.teen_range}"
    
    @property
    def total_attendance(self):
        return self.attendances.count()

class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendances')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='attendances')
    village = models.CharField(max_length=255)
    new_in_teen = models.BooleanField()
    PURPOSE_CHOICES = [
        ('Clinic', 'Clinic'),
        ('Support', 'Support')
    ]
    purpose = models.CharField(max_length=7, choices=PURPOSE_CHOICES)
    guardian_present = models.BooleanField()
    SCHOOL_CHOICES = [
        ('No','No'),
        ('Yes, Day', 'Yes, Day'),
        ('Yes, BRD', 'Yes, BRD')
    ]
    school = models.CharField(max_length=8, choices=SCHOOL_CHOICES)
    vl_drawn = models.BooleanField()
    notes = models.TextField(blank=True, null=True)
    arrived_at = models.TimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-arrived_at']
        unique_together = ['session', 'patient']

    def __str__(self):
        return f"{self.patient.arv_number}, Purpose: {self.purpose}"
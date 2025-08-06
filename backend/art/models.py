from django.db import models
from pact.models import Patient

class ChildVisit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='artvisits')
    visit_date = models.DateField(null=True, blank=True)

    VISIT_TYPE_CHOICES = [
        ('Patient Only', 'Patient Only'),
        ('Guardian Only', 'Guardian Only'),
        ('Both Patient & Guardian', 'Both Patient & Guardian')
    ]

    visit_type = models.CharField(max_length=50, choices=VISIT_TYPE_CHOICES, default='Patient Only')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    SIDE_EFFECT_CHOICES = [
        ('NO', 'NO'),
        ('PN', 'PN'),
        ('HP', 'HP'),
        ('SK', 'SK'),
        ('LIP', 'LIP'),
        ('OTH', 'OTH')
    ]

    side_effect = models.CharField(max_length=3, choices=SIDE_EFFECT_CHOICES, default='NO')
    TB_STATUS_CHOICES = [
        ('N', 'N'),
        ('Y', 'Y'),
        ('C', 'C'),
        ('Rx', 'Rx')
    ]

    tab_status = models.CharField(max_length=2, choices=TB_STATUS_CHOICES, default="N")
    VIRAL_LOAD_CHOICES = [
        ('Not Bled', 'Not Bled'),
        ('BLED', 'BLED'),
        ('Result', 'Result')
    ]
    viral_load = models.CharField(max_length=50, choices=VIRAL_LOAD_CHOICES, default= 'Not Bled')
    pill_count = models.IntegerField(null=True, blank=True)
    regimen = models.CharField(max_length=4)
    REGIMEN_CHOICES = [
        ('1A', '')
    ]
    arv_given = models.IntegerField()
    cpt_given = models.IntegerField()
    TPT_CHOICES = [
        ('Not Given', 'Not Given'),
        ('3HP', '3HP'),
        ('INH', 'INH')
    ]
    tpt_given = models.CharField(max_length=9, choices=TPT_CHOICES,default='Not Given', null=True, blank=True)
    tpt_amount = models.IntegerField(null=True, blank=True)
    next_outcome_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['patient', 'visit_date'], name='unique_patient_visit')
        ]
    def __str__(self):
        return f"{self.patient.arv_number}: {self.patient.name}, Visit Date: {self.visit_date}"
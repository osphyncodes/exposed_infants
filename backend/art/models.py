from django.db import models
from pact.models import Patient

class ChildVisit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient')
    visit_date = models.DateField(null=True, blank=True)

    VISIT_TYPE_CHOICES = [
        'Patient Only',
        'Guardian Only',
        'Both Patient & Guardian'
    ]
    visit_type = models.CharField(choices=VISIT_TYPE_CHOICES)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    WASTING_CHOICES = [
        ('No', 'No Wasting'), ('Mod', 'Moderate'), ('Sev', 'Severe')
    ]
    wasting = models.CharField(max_length=4, choices=WASTING_CHOICES, null=True, blank=True, default='No')

    BREASTFEEDING_CHOICES = [
        ('Exc', 'Exclusive'), ('M', 'Mixed/Complement'), ('<6', 'Stopped last 6 Weeks'),
        ('C', 'Stopped over 6w. ago')
    ]
    breastfeeding = models.CharField(max_length=10, choices=BREASTFEEDING_CHOICES, null=True, blank=True, default='Exc')

    MOTHER_ART_CHOICES = [
        ('No ART', 'Alive No ART'),
        ('On ART', 'Alive On ART'),
        ('Died', 'Died'),
        ('Unk', 'Unknown')
    ]
    mother_art_status = models.CharField(max_length=10, choices=MOTHER_ART_CHOICES, null=True, blank=True, default='On ART')

    CLINICAL_MONITORING_CHOICES = [
        ('NAD', 'No Abnormality Detected'),
        ('Sick', 'Sick child')
    ]
    clinical_monitoring = models.CharField(max_length=10, choices=CLINICAL_MONITORING_CHOICES, null=True, blank=True, default='NAD')

    HIV_TEST_CHOICES = [
        ('No', 'Not done'),
        ('Dbs', 'Dried Blood Spot (PCR)'),
        ('Rt', 'Rapid Test')
    ]
    hiv_testing = models.CharField(max_length=10, choices=HIV_TEST_CHOICES, null=True, blank=True, default='No')

    HIV_INFECTION_STATUS_CHOICES = [
        ('A', 'Not Infected'),
        ('B', 'Infected'),
        ('C', 'Not ART Eligible'),
        ('D', 'PSHD -> ART')
    ]
    infection_status = models.CharField(max_length=20, choices=HIV_INFECTION_STATUS_CHOICES, null=True, blank=True, default='C')

    DRUG_GIVEN_CHOICES = [
        ('None', 'No Drugs Given'),
        ('CPT', 'Cotrimoxazole Prophylaxis (CPT)'),
        ('NVP', 'Nevirapine (NVP)'),
        ('2P', '2P'),
    ]
    drug_given = models.CharField(max_length=10, choices=DRUG_GIVEN_CHOICES, null=True, blank=True, default='CPT')

    cpt_given = models.PositiveIntegerField(null=True, blank=True, help_text="Number of CPT/NVP tablets given")

    FOLLOW_UP_CHOICES = [
        ('Con', 'Continue FUP'),
        ('Dis', 'Discharged'),
        ('ART', 'Started ART'),
        ('To', 'Transferred Out'),
        ('Def', 'Defaulted'),
        ('Died', 'Died')
    ]
    follow_up_outcome = models.CharField(max_length=10, choices=FOLLOW_UP_CHOICES,default='Con', null=True, blank=True)

    art_number = models.IntegerField(null=True, blank=True)

    next_appointment_or_outcome_date = models.DateField(null=True, blank=True)

    def age_in_months(self):
        # Calculate age in months at the time of visit
        if self.child.child_dob and self.visit_date:
            return (self.visit_date.year - self.child.child_dob.year) * 12 + (self.visit_date.month - self.child.child_dob.month)
        return "?"

    def __str__(self):
        return f"{self.child.child_name} - {self.visit_date} - {self.age_in_months()} months"
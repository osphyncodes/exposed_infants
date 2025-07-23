from django.db import models

class Child(models.Model):
    hcc_number = models.CharField(max_length=20, primary_key=True)
    child_name = models.CharField(max_length=200)
    child_dob = models.DateField()

    CHILD_GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    child_gender = models.CharField(max_length=6, choices=CHILD_GENDER_CHOICES)

    child_birth_weight = models.DecimalField(max_digits=5, decimal_places=2)
    guardian_name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100, default='Mother')
    guardian_phone = models.CharField(max_length=20, default='None')
    physical_address = models.TextField()
    
    AGREES_TO_FUP_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    agrees_to_fup = models.CharField(max_length=3, choices=AGREES_TO_FUP_CHOICES, default='Yes')

    MOTHER_STATUS_CHOICES = [
        ('Alive No ART', 'Alive No ART'),
        ('Alive OnART', 'Alive OnART'),
        ('Died', 'Died'),
        ('Unknown', 'Unknown'),
    ]
    mother_status = models.CharField(max_length=20, choices=MOTHER_STATUS_CHOICES, default='Alive OnART')
    mother_art_number = models.CharField(max_length=20, blank=True, null=True)
    mother_art_start_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.child_name} ({self.hcc_number})"
    

class ChildVisit(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateField(null=True, blank=True)

    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    muac = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

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

class HTSSample(models.Model):
    TEST_TYPE_CHOICES = [
        ('DBS', 'Dried Blood Spot'),
        ('Rapid', 'Rapid Test'),
    ]

    RESULT_CHOICES = [
        ('Negative', 'Negative'),
        ('Positive', 'Positive'),
        ('Inconclusive', 'Inconclusive'),
    ]

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='hts_samples')
    sample_date = models.DateField()
    test_type = models.CharField(max_length=10, choices=TEST_TYPE_CHOICES)

    REASON_CHOICES = [
        ('DBS_6wks_Ini', 'DBS 6 Weeks Initial'),
        ('DBS_6wks_Con', 'DBS 6 Weeks Confirmatory'),
        ('DBS_Rapid_Conf', 'DBS Rapid Confirmatory'),
        ('Rapid_1yr', 'Rapid @ 1yr'),
        ('Rapid_2yr', 'Rapid @ 2yr'),
    ]

    reason = models.CharField(max_length=30, choices=REASON_CHOICES, null=True, blank=True)
    sample_id = models.CharField(max_length=50)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, null=True, blank=True)
    date_received = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.child.child_name} - {self.test_type} - {self.result}"


# --- System Log Model ---
from django.contrib.auth.models import User

class SystemLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('add', 'Add'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action}"


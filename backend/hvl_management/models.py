from django.db import models
from pact.models import Staff

class HVLRecord(models.Model):
    sn = models.IntegerField("Serial Number", unique=True, primary_key=True)
    art_number = models.IntegerField("ART Number")
    sex = models.CharField("Sex", max_length=10)
    age = models.IntegerField("Age")
    date_entered = models.DateField("Date Entered")
    sample_log_number = models.IntegerField("Sample Log Number")
    reason_for_test = models.CharField("Reason for Test", max_length=100)
    result_value = models.IntegerField("Result Value")
    status = models.CharField("Status", max_length=50, blank=True, null=True)
    
    def has_iac(self):
        if IacSession.objects.filter(hvl_record=self).exists():
            return "Yes"
        else:
            return "No"
        
    def iac_date(self):
            session = IacSession.objects.filter(hvl_record=self)
            
            if session.exists():
                return session.first().session_date
        
        
    def has_iac_followup(self):
        if IacFollowUp.objects.filter(hvl_record=self).exists():
            return "Yes"
        else:
            return "No"

    def __str__(self):
        return f"HVL Record SN: {self.pk} - ART Number: {self.art_number}"

class IacSession(models.Model):
    hvl_record = models.ForeignKey(HVLRecord, on_delete=models.CASCADE, related_name='iac_sessions')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    session_date = models.DateField()
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"IAC Session for HVL Record SN: {self.hvl_record.sn} - Staff: {self.staff} - Ended at: {self.end_time}"
    
class IacFollowUp(models.Model):
    hvl_record = models.ForeignKey(HVLRecord, on_delete=models.CASCADE, related_name='iac_follow_ups')
    collection_date = models.DateField()
    sample_log_number = models.IntegerField("Sample Log Number")
    result_value = models.CharField("Result Value", max_length=100, null=True, blank=True)
    date_given_to_client = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"IAC Follow-Up on {self.collection_date} for HVL Record SN: {self.hvl_record.sn}"
    
# model for drug resistance testing
class DrugResistanceApplication(models.Model):
    hvl_record = models.ForeignKey(HVLRecord, on_delete=models.CASCADE, related_name='drug_resistance_tests')
    application_date = models.DateField()
    submit_sample = models.CharField(max_length=100, default="Pending", choices=[
        ('Pending', 'Pending'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    ], verbose_name="Committee Advice: Submit Sample?")
    collection_date = models.DateField(null=True, blank=True)
    resistance_detected = models.CharField(max_length=100, default="Pending", choices=[
        ('Pending', 'Pending'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    ], verbose_name="Resistance Detected")
    action_taken = models.CharField("Action Taken", max_length=100, blank=True, null=True, choices=[
        ('switch', 'Switch Regimen'),
        ('continue', 'Continue Current Regimen'),
    ])
    # Viral load 6 months after action taken
    vl_after_action = models.CharField("Viral Load 6 Months After Action",max_length=100, blank=True, null=True)

    comments = models.TextField("Comments", blank=True, null=True)

    def __str__(self):
        return f"Drug Resistance Application on {self.application_date} for HVL Record SN: {self.hvl_record.sn}"

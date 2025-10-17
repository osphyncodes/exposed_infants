from django.db import models

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

    def __str__(self):
        return f"HVL Record SN: {self.pk} - ART Number: {self.art_number}"

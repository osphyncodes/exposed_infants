from django.db import models, transaction
from io import StringIO
import csv
from pact.models import Patient # Assuming this is where your ART Patients model is

class ClientCard(models.Model):
    CARD_TYPES = [
        ('hvl', 'HVL Client Card'),
        ('b2c', 'Back to Care Client Card'),
        ('new_initiation', 'New Initiation Client Card'),
    ]
    
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('Complete', 'Complete'),
        ('DIED', 'Died'),
        ('TRANSFERRED', 'Transferred Out'),
        ('STOPPED', 'Treatment Stopped'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=100, unique=True)
    card_type = models.CharField(max_length=14, choices=CARD_TYPES)
    date_opened = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='IN_PROGRESS')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_card_type_display()} - {self.patient.name}: {self.patient.arv_number}"
    
    @classmethod
    def import_client_card(cls, csv_file, chunk_size=5000):
        results = {
            'deleted': 0,
            'created': 0,
            'errors': []
        }


        # First delete ALL existing records
        with transaction.atomic():
            deleted_count, _ = cls.objects.all().delete()
            results['deleted'] = deleted_count

        # Then import all new records from CSV
        file_content = csv_file.read().decode('utf-8')
        reader = csv.DictReader(StringIO(file_content))
        
        to_create = []
        
        for row in reader:
            arv_num = row.get('art_number', '')

            if arv_num:
                patient = Patient.objects.filter(arv_number = arv_num)

                # Check patient exists (if needed)
                if not patient.exists():
                    results['errors'].append({
                        'row': row,
                        'error': f"Patient ARV#{arv_num} not found"
                    })
                    continue

                client_card = cls(
                    patient=patient.first(),
                    card_type=row.get('card_type', ''),
                    unique_id=row.get('unique_id', ''),
                    date_opened=row.get('date_enrollment', ''),
                    status=row.get('status', ''),
                )

                to_create.append(client_card)

            else:
                results['errors'].append({
                    'row': row,
                    'error': "Invalid ARV number"
                })
                continue

        with transaction.atomic():
            cls.objects.bulk_create(to_create)
            results['created'] = len(to_create)
        return results

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
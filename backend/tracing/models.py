from django.db import models, transaction
from pact.models import Staff
from io import StringIO
import csv


class Tracing(models.Model):
    unique_id = models.IntegerField(primary_key=True)
    chw = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="tracings")
    date_entered = models.DateTimeField()
    art_number = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    with_phone = models.BooleanField(default=False)
    tracing_attempted = models.BooleanField(default=False)
    by_motorbike = models.BooleanField(default=False)
    home_traced = models.BooleanField(default=False)
    phone_called = models.BooleanField(default=False)
    tracing_outcome = models.BooleanField(default=False)
    final_outcome = models.CharField(max_length=100)
    outcome_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.art_number}->{self.chw.name}->{self.reason}"
    
    @classmethod
    def import_tracing_csv(cls, csv_file):
        from io import TextIOWrapper
        results = {'created': 0, 'updated': 0, 'unchanged': 0, 'errors': []}
        
        try:
            # Read entire file into memory
            content = TextIOWrapper(csv_file.file, encoding='utf-8').read()
            
            # First pass to get all unique_ids for the query
            reader = csv.DictReader(StringIO(content))
            unique_ids = []
            for row in reader:
                try:
                    unique_ids.append(int(row['unique_id']))
                except (ValueError, KeyError):
                    continue
            
            # Get existing records in one query
            existing_tracing = {
                p.unique_id: p
                for p in cls.objects.filter(unique_id__in=unique_ids)
            }
            
            # Reset reader for actual processing
            reader = csv.DictReader(StringIO(content))
            
            to_create = []
            to_update = []
            
            for row in reader:
                try:
                    unique_id = int(row['unique_id'])

                    staff = Staff.objects.get(chw_code=row['chw_id'])
                    if not staff:
                        results['errors'].append({
                            'row': row,
                            'error': 'CHW not found'
                        })
                        continue
                    
                    tracing_data = {
                        'chw': staff,
                        'date_entered': row['date_entered'],  # Note: Typo in field name?
                        'art_number': row['art_number'],
                        'type': row['type'],
                        'reason': row['reason'],
                        'with_phone': row.get('with_phone', '').lower() == 'yes',
                        'home_traced': row.get('home_traced', '').lower() == 'home traced',
                        'tracing_outcome': row.get('tracing_outcome', '').lower() == 'talked to',
                        'final_outcome': row['final_outcome']
                    }

                    

                    if unique_id in existing_tracing:
                        existing = existing_tracing[unique_id]
                        needs_update = False
                        update_fields = []

                        for field, value in tracing_data.items():
                            current_value = getattr(existing, field, None)
                            if current_value != value:
                                setattr(existing, field, value)
                                update_fields.append(field)
                                needs_update = True

                        if needs_update:
                            to_update.append(existing)
                            results['updated'] += 1
                        else:
                            results['unchanged'] += 1
                    else:
                        print(tracing_data)
                        to_create.append(cls(unique_id=unique_id, **tracing_data))
                        results['created'] += 1

                except Exception as e:
                    results['errors'].append({
                        'row': row,
                        'error': str(e)
                    })
                    continue
            
            # Bulk operations
            with transaction.atomic():
                if to_create:
                    cls.objects.bulk_create(to_create)
                if to_update:
                    # Get all fields that might need updating
                    fields = ['chw', 'date_entered', 'type', 'reason', 
                            'with_phone', 'home_traced', 'tracing_outcome', 'final_outcome']
                    cls.objects.bulk_update(to_update, fields)

            return results
            
        except Exception as e:
            results['errors'].append({
                'error': f"File processing error: {str(e)}"
            })
            return results
        
class HomeTracing(models.Model):
    HOME_TRACING_CHOICES = [
        ('found_house_talked', 'Found House and Talked to Client'),
        ('found_house_not_home', 'Found House but Client Not Home'),
        ('house_not_found', 'House Not Found')

    ]
    tracing = models.ForeignKey(Tracing, on_delete=models.CASCADE, related_name="home_tracings")
    date_visited = models.DateTimeField()
    outcome = models.CharField(max_length=100, choices=HOME_TRACING_CHOICES)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'hometracing'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Tracing.objects.filter(unique_id=self.tracing.unique_id).update(home_traced=True)
        Tracing.objects.filter(unique_id=self.tracing.unique_id).update(tracing_attempted=True)
        if self.outcome == 'found_house_talked':
            Tracing.objects.filter(unique_id=self.tracing.unique_id).update(tracing_outcome=True)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if not HomeTracing.objects.filter(tracing=self.tracing).exists():
            Tracing.objects.filter(unique_id=self.tracing.unique_id).update(home_traced=False)
            if not PhoneTracing.objects.filter(tracing__unique_id=self.tracing.unique_id).exists():
                Tracing.objects.filter(unique_id=self.tracing.unique_id).update(tracing_attempted=False)

        if not HomeTracing.objects.filter(tracing__unique_id=self.tracing.unique_id, outcome='found_house_talked').exists():
            if not PhoneTracing.objects.filter(tracing__unique_id=self.tracing.unique_id, outcome='talked_to_client').exists():
                Tracing.objects.filter(unique_id=self.tracing.unique_id).update(tracing_outcome=False)


class PhoneTracing(models.Model):
    PHONE_CALL_RESULT_CHOICES = [
        ('talked_to_client', 'Talked to Client'),
        ('wrong_number', "wrong Number/Didn't Know Client"),
        ('no_answer', 'No Answer'),
        ('out_of_network', 'Out of Network'),
        ('line_busy', 'Line Busy')
    ]
    tracing = models.ForeignKey(Tracing, on_delete=models.CASCADE, related_name="phone_tracings")
    date_called = models.DateTimeField()
    outcome = models.CharField(max_length=100, choices=PHONE_CALL_RESULT_CHOICES)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'phonetracing'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Tracing.objects.filter(unique_id=self.tracing.unique_id).update(phone_called=True)
        Tracing.objects.filter(unique_id=self.tracing.unique_id).update(tracing_attempted=True)
        if self.outcome == 'talked_to_client':
            Tracing.objects.filter(unique_id=self.tracing.unique_id).update(tracing_outcome=True)

    def delete(self, *args, **kwargs):
        tracing_id = self.tracing.unique_id
        super().delete(*args, **kwargs)
        if not PhoneTracing.objects.filter(tracing__unique_id=tracing_id).exists():
            Tracing.objects.filter(unique_id=tracing_id).update(phone_called=False)
            if not HomeTracing.objects.filter(tracing__unique_id=tracing_id).exists():
                Tracing.objects.filter(unique_id=tracing_id).update(tracing_attempted=False)

        if not PhoneTracing.objects.filter(tracing__unique_id=tracing_id, outcome='talked_to_client').exists():
            if not HomeTracing.objects.filter(tracing__unique_id=tracing_id, outcome='found_house_talked').exists():
                Tracing.objects.filter(unique_id=tracing_id).update(tracing_outcome=False)
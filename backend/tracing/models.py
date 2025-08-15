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
    home_traced = models.BooleanField(default=False)
    tracing_outcome = models.BooleanField(default=False)
    final_outcome = models.CharField(max_length=100)

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

                    staff = Staff.objects.get(id=row['chw_id'])
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
from celery import shared_task
from pact.models import Patient, LabResult
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay, Now, Replace
from django.db.models import Count, Q, F, Value, IntegerField, Case, When
from django.utils import timezone


@shared_task
def process_data():
    today = timezone.now().date()
    
    # Common age annotation for all queries
    age_annotation = {
        'birth_month': ExtractMonth(F('birthdate')),
        'birth_day': ExtractDay(F('birthdate')),
        'current_month': ExtractMonth(Now()),
        'current_day': ExtractDay(Now()),
        'age': ExtractYear(Now()) - ExtractYear(F('birthdate')) - 
            Case(
                When(
                    Q(birth_month__gt=F('current_month')) |
                    (Q(birth_month=F('current_month')) & 
                     Q(birth_day__gt=F('current_day'))),
                    then=Value(1)
                ),
                default=Value(0),
                output_field=IntegerField()
            )
    }

    # 1. Total children < 20 years on ART
    children = Patient.objects.under_age(20).filter(outcome = 'On antiretrovirals').all()
    
    children_total = children.count()
    
    recent_count = 0
    suppressed_count = 0
    high_count = 0

    for child in children:
        arv_number = child.arv_number
        results = LabResult.objects.filter(
            arv_number = arv_number
        ).order_by('-order_date').first()

        if results and results.result:
            # recent result count
            recent_count += 1

            result = results.result
            result = clean_string(result)
            intvalue = can_convert_to_int(result)
            
            if intvalue:
                if int(result)>= 1000:
                    high_count += 1
                else:
                    suppressed_count += 1
            else:
                if result.upper() == 'LDL':
                    suppressed_count += 1

    context = {
        'children_on_art': children_total,
        'recent_vl_count': recent_count,
        'suppressed_vl': suppressed_count,
        'high_vl': high_count,
    }

    return context

def clean_string(input_string):
    # Remove <, >, and = characters from the string
    return input_string.replace('<', '').replace('>', '').replace('=', '')

def can_convert_to_int(input_string):
    try:
        int(input_string)  # Try to convert string to int
        return True
    except ValueError:  # If conversion fails, it raises a ValueError
        return False
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Count, Q, F, Value
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Patient, LabResult, Regimen
from django.db.models.functions import Replace





@login_required
def children_view(request):
    """
    Render the Pact children view.
    """
    return render(request, 'pact/children.html')

@login_required
def reports(request):
    """
    Render the Pact reports view.
    """
    return render(request, 'pact/reports.html')

@login_required
def reminders(request):
    """
    Render the Pact reminders view.
    """
    return render(request, 'pact/reminders.html')

@login_required
def import_export(request):
    """
    Render the Pact import/export view.
    """
    return render(request, 'pact/import_export.html')

@login_required
def logs(request):
    """
    Render the Pact logs view.
    """
    return render(request, 'pact/logs.html')

@login_required
def user_management(request):
    """
    Render the Pact user management view.
    """
    return render(request, 'pact/user_management.html')

@login_required
def add_user(request):
    """
    Render the Pact add user view.
    """
    return render(request, 'pact/add_user.html')

@login_required
def edit_user(request, user_id):
    """
    Render the Pact edit user view.
    """
    return render(request, 'pact/edit_user.html', {'user_id': user_id})

@login_required
def delete_user(request, user_id):
    """
    Render the Pact delete user view.
    """
    return render(request, 'pact/delete_user.html', {'user_id': user_id})   

@login_required
def change_password(request):
    """
    Render the Pact change password view.
    """
    return render(request, 'pact/change_password.html')

@csrf_exempt
def import_patients(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        # Check file extension
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({
                'status': 'error',
                'message': 'Please upload a CSV file'
            }, status=400)
        
        # Process the CSV file
        results = Patient.import_from_csv(csv_file)
        
        return JsonResponse({
            'status': 'success',
            'results': results
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method or no file uploaded'
    }, status=400)

@csrf_exempt
def import_lab_results(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({
                'status': 'error',
                'message': 'Please upload a CSV file'
            }, status=400)
        
        results = LabResult.import_large_csv(csv_file)
        
        return JsonResponse({
            'status': 'success',
            'results': results
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method or no file uploaded'
    }, status=400)

def lab_import_view(request):
    return render(request, 'pact/imports/result_import.html')

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Patient, Regimen
import csv
from io import StringIO
from django.db import transaction

@csrf_exempt
def import_patient_data(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({
                'status': 'error',
                'message': 'Please upload a CSV file'
            }, status=400)
        
        results = Regimen.import_regimen_data(csv_file)
        
        return JsonResponse({
            'status': 'success',
            'results': results
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method or no file uploaded'
    }, status=400)

def import_view(request):
    return render(request, 'pact/imports/regimen.html')



from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay, Now, Replace
from django.db.models import Count, Q, F, Value, IntegerField, Case, When


def pact_dashboard(request):
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
    children_on_art = Patient.objects.under_age(20).filter(outcome = 'On antiretrovirals').count()
    #children_on_art = Patient.objects.under_age(20).count()

    # 2. Total children with recent VL results
    recent_vl_count = LabResult.objects.filter(
        result__isnull=False,
        arv_number__in=Patient.objects.under_age(20).filter(outcome = 'On antiretrovirals').values('arv_number')
    ).order_by('-order_date').values('arv_number').distinct().count()
    
    # 3. Total children with suppressed VL
    suppressed_vl = LabResult.objects.filter(
        result__isnull=False,
        arv_number__in=Patient.objects.under_age(20).filter(outcome = 'On antiretrovirals').values('arv_number')
    ).annotate(
        clean_result=Replace(
            Replace(
                Replace('result', Value('='), Value('')), 
                Value('<'), Value('')), 
            Value('>'), Value(''))
    ).filter(
        Q(clean_result__iexact='LDL') | 
        Q(clean_result__lt=1000)
    ).values('arv_number').distinct().count()
    
    # 4. Total children with high VL
    high_vl = LabResult.objects.filter(
        result__isnull=False,
        arv_number__in=Patient.objects.annotate(
            **age_annotation
        ).filter(age__lt=20).values('arv_number')
    ).annotate(
        clean_result=Replace(
            Replace(
                Replace('result', Value('='), Value('')), 
                Value('<'), Value('')), 
            Value('>'), Value(''))
    ).exclude(
        Q(clean_result__iexact='LDL') | 
        Q(clean_result__lt=1000)
    ).values('arv_number').distinct().count()
    
    # 5. Age band distribution
    age_bands = [
        ('0-4', (0, 4)),
        ('5-9', (5, 9)),
        ('10-14', (10, 14)),
        ('15-19', (15, 19))
    ]
    
    age_data = []
    for label, (min_age, max_age) in age_bands:
        # Get suppressed count for age band
        suppressed = LabResult.objects.filter(
            result__isnull=False,
            arv_number__in=Patient.objects.annotate(
                **age_annotation
            ).filter(
                age__gte=min_age,
                age__lte=max_age
            ).values('arv_number')
        ).annotate(
            clean_result=Replace(
                Replace(
                    Replace('result', Value('='), Value('')), 
                    Value('<'), Value('')), 
                Value('>'), Value(''))
        ).filter(
            Q(clean_result__iexact='LDL') | 
            Q(clean_result__lt=1000)
        ).count()
        
        # Get high VL count for age band
        high = LabResult.objects.filter(
            result__isnull=False,
            arv_number__in=Patient.objects.annotate(
                **age_annotation
            ).filter(
                age__gte=min_age,
                age__lte=max_age
            ).values('arv_number')
        ).annotate(
            clean_result=Replace(
                Replace(
                    Replace('result', Value('='), Value('')), 
                    Value('<'), Value('')), 
                Value('>'), Value(''))
        ).exclude(
            Q(clean_result__iexact='LDL') | 
            Q(clean_result__lt=1000)
        ).count()
        
        age_data.append({
            'age_band': label,
            'suppressed': suppressed,
            'high_vl': high
        })
    
    # 6. Gender distribution
    gender_data = Patient.objects.annotate(
        **age_annotation
    ).filter(
        age__lt=20
    ).values('gender').annotate(
        total=Count('id'),
        suppressed=Count('labresult', filter=Q(
            labresult__result__isnull=False,
            labresult__result__regex=r'^(<|=)?(LDL|\d+)$',
            labresult__result__in=['LDL', '<1000']
        )),
        high_vl=Count('labresult', filter=Q(
            labresult__result__isnull=False
        ) & ~Q(
            labresult__result__in=['LDL', '<1000']
        ))
    )
    
    context = {
        'children_on_art': children_on_art,
        'recent_vl_count': recent_vl_count,
        'suppressed_vl': suppressed_vl,
        'high_vl': high_vl,
        'age_data': age_data,
        'gender_data': list(gender_data),
        'high_vl_patients': LabResult.objects.filter(
            result__isnull=False,
            arv_number__in=Patient.objects.annotate(
                **age_annotation
            ).filter(age__lt=20).values('arv_number')
        ).annotate(
            clean_result=Replace(
                Replace(
                    Replace('result', Value('='), Value('')), 
                    Value('<'), Value('')), 
                Value('>'), Value(''))
        ).exclude(
            Q(clean_result__iexact='LDL') | 
            Q(clean_result__lt=1000)
        ).select_related('arv_number')[:50],
        'pending_results': LabResult.objects.filter(
            result__isnull=True,
            arv_number__in=Patient.objects.annotate(
                **age_annotation
            ).filter(age__lt=20).values('arv_number')
        ).order_by('-order_date').select_related('arv_number')[:50]
    }
    return render(request, 'pact/pact_dashboard.html', context)
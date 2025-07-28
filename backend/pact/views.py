from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator
from django.db.models import Count, Q, F, Value, IntegerField, Case, When
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Patient, LabResult, Regimen
from collections import defaultdict
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay, Now, Replace


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


def pact_dashboards(request):
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
    age_bands_high = [
        ('0-4', (0, 4)),
        ('5-9', (5, 9)),
        ('10-14', (10, 14)),
        ('15-19', (15, 19))
    ]
    
    age_data = []
    for label, (min_age, max_age) in age_bands_high:
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

def pact_dashboard(request):
    # 1. Total children < 20 years on ART
    children = Patient.objects.filter(outcome = 'On antiretrovirals').all()
    
    children_total = 0
    recent_count = 0
    suppressed_count = 0
    high_count = 0
    cons_high_total = 0


    high_vl_clients = []
    cons_high_vl_clients = []

    age_bands_high = defaultdict(int)
    age_bands_supp = defaultdict(int)
    age_bands_recent = defaultdict(int)

    gender_bands_high = defaultdict(int)
    gender_bands_supp = defaultdict(int)
    gender_bands_recent = defaultdict(int)

    for child in children:
        age = child.age()
        gender = child.gender
        cons_high_count = 0

        cons_results = {
            'result1': None,
            'result2': None,
            'result3': None
        }

        if age <= 19:
            #total children count
            children_total += 1

            arv_number = child.arv_number

            latest_result = LabResult.objects.filter(
                arv_number = arv_number
            ).order_by('-order_date').first()

            curr_results = LabResult.objects.filter(
                arv_number = arv_number,
                result__isnull = False
            ).order_by('-order_date').all()

            if curr_results.count() >= 3:
                curr_results = curr_results[:3]
                for curr_result in curr_results:
                    resultc = clean_string(curr_result.result)
                    if can_convert_to_int(resultc) and int(resultc) >= 1000 and cons_high_count <=3:
                        cons_high_count += 1

                        cons_results[f"result{cons_high_count}"] = f"Order Date: {curr_result.order_date}, Result: {resultc}"


                if cons_high_count == 3:
                    cons_high_total += 1
                    print(curr_result)
                    cons_high_vl_clients.append(childObject(child=child, result=curr_result, age=age, cons_results = cons_results))


            if latest_result and latest_result.result:
                # recent result count
                recent_count += 1
                ageBandDict(age_bands_recent, age)
                genderDict(gender_bands_recent, gender)

                result = latest_result.result
                result = clean_string(result)
                intvalue = can_convert_to_int(result)
                
                if intvalue:
                    if int(result)>= 1000:
                        high_count += 1
                        ageBandDict(age_bands_high, age)
                        genderDict(gender_bands_high, gender)
                        high_vl_clients.append(childObject(child=child, result=latest_result, age=age))
                    else:
                        suppressed_count += 1
                        ageBandDict(age_bands_supp, age)
                        genderDict(gender_bands_supp, gender)
                else:
                    if result.upper() == 'LDL':
                        suppressed_count += 1
                        ageBandDict(age_bands_supp,age)
                        genderDict(gender_bands_supp, gender)

    my_array = [i for i in high_vl_clients]
    items, paginator = paginate_array(request, my_array)

    my_array2 =[i for i in cons_high_vl_clients]
    items2, paginator2 = paginate_array(request, my_array2)

    context = {
        'children_on_art': children_total,
        'recent_vl_count': recent_count,
        'suppressed_vl': suppressed_count,
        'high_vl': high_count,
        'high_age_band': age_bands_high,
        'supp_age_band': age_bands_supp,
        'recent_age_band': age_bands_recent,
        'high_gender_band': gender_bands_high,
        'supp_gender_band': gender_bands_supp,
        'recent_gender_band': gender_bands_recent,
        'high_vl_clients': items,
        'cons_high': items2,
        'cons_high_count': cons_high_total
    }
    return render(request, 'pact/pact_dashboard.html', context)

def clean_string(input_string):
    # Remove <, >, and = characters from the string
    return input_string.replace('<', '').replace('>', '').replace('=', '')

def can_convert_to_int(input_string):
    try:
        int(input_string)  # Try to convert string to int
        return True
    except ValueError:  # If conversion fails, it raises a ValueError
        return False
    
def ageBandDict(dictionary, age):
    if 0 <= age <= 4:
        dictionary['0_4'] += 1
    elif 5 <= age <= 9:
        dictionary['5_9'] += 1
    elif 10 <= age <= 14:
        dictionary['10_14'] += 1
    elif 15 <= age <= 19:
        dictionary['15_19'] += 1
    
    return dictionary

def genderDict(dictionary, gender):
    if gender == 'Male':
        dictionary['male'] += 1
    elif gender == 'Female':
        dictionary['female'] += 1
    
    return dictionary

def childObject(child, result, age, cons_results = None):
    data = {
        'arv_number': child.arv_number,
        'age': age,
        'gender': child.gender,
        'order_date': result.order_date,
        'result': clean_string(result.result),
        'result_date': result.date_received,
        'cons_results': cons_results
    }
    return data

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_array(request, array, items_per_page=5):
    paginator = Paginator(array, items_per_page)
    page = request.GET.get('page')
    
    try:
        paginated_items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        paginated_items = paginator.page(paginator.num_pages)
    
    return paginated_items, paginator

def children_view(request):
    children_list =  Patient.objects.under_age(20).filter(outcome = 'On antiretrovirals').all()
    

    childrens = []
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            children_list = children_list.filter(arv_number__icontains=query)
    

    # Get per_page from GET
    per_page = request.GET.get('per_page', '10')
    
    if per_page == 'all':
        page_obj = children_list  # Not paginated
        is_paginated = False
    else:
        try:
            per_page = per_page
        except ValueError:
            per_page = '10'
            # per_page = 10
        paginator = Paginator(children_list, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        is_paginated = True

    print(len(children_list))
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
        'is_paginated': is_paginated,
    }
    return render(request, 'pact/children.html', context)

@login_required
def children_dashboard_view(request, art_number):

    return render(request, 'pact/child_dashboard.html')
